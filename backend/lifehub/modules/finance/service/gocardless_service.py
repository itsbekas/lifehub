import datetime as dt
from typing import Optional

from sqlalchemy.orm import Session

from lifehub.core.common.base.service.user import BaseUserService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.security.encryption import EncryptionService
from lifehub.core.user.schema import User
from lifehub.modules.finance.models import BankInstitutionResponse
from lifehub.modules.finance.repository import BankAccountRepository
from lifehub.modules.finance.schema import BankAccount, BankTransaction
from lifehub.providers.gocardless.api_client import GoCardlessAPIClient
from lifehub.providers.gocardless.models import Transaction


class GoCardlessServiceException(ServiceException):
    def __init__(self, status_code: int, message: str):
        super().__init__("GoCardless", status_code, message)


class GoCardlessService(BaseUserService):
    _encryption_service: EncryptionService | None = None
    _gocardless_api: GoCardlessAPIClient | None = None

    def __init__(self, session: Session, user: User):
        super().__init__(session, user)

    @property
    def encryption_service(self) -> EncryptionService:
        if self._encryption_service is None:
            self._encryption_service = EncryptionService(self.session, self.user)
        return self._encryption_service

    @property
    def gocardless_api(self) -> GoCardlessAPIClient:
        if self._gocardless_api is None:
            self._gocardless_api = GoCardlessAPIClient(self.user, self.session)
        return self._gocardless_api

    def get_institutions(self, country: str) -> list[BankInstitutionResponse]:
        """
        Fetches a list of institutions available in the specified country.
        """
        api = GoCardlessAPIClient(self.user, self.session)
        return [
            BankInstitutionResponse(
                id=inst.id,
                type="oauth",
                name=inst.name,
                logo=inst.logo,
            )
            for inst in api.get_institutions(country)
        ]

    def get_bank_login(self, bank_id: str) -> str:
        api = GoCardlessAPIClient(self.user, self.session)
        return api.create_requisition(bank_id).link

    def confirm_bank_login(self, ref: str) -> None:
        api = GoCardlessAPIClient(self.user, self.session)
        requisition = api.get_requisition(ref)
        bank_account_repo = BankAccountRepository(self.user, self.session)
        for account_id in requisition.accounts:
            encrypted_account_id = self.encryption_service.encrypt_data(account_id)
            bank_account = BankAccount(
                user_id=self.user.id,
                account_id=encrypted_account_id,
                institution_id=self.encryption_service.encrypt_data(
                    requisition.institution_id
                ),
                requisition_id=self.encryption_service.encrypt_data(ref),
            )
            bank_account_repo.add(bank_account)

        self.session.commit()

    def fetch_balance(self, account: BankAccount) -> Optional[float]:
        """
        Fetches the latest balance from GoCardless.
        """
        balance = (
            GoCardlessAPIClient(self.user, self.session)
            .get_account_balances(
                self.encryption_service.decrypt_data(account.account_id)
            )
            .available_amount
        )
        return float(balance) if balance is not None else None

    def _parse_transactions(
        self, account: BankAccount, api_transactions: list[Transaction]
    ) -> list[BankTransaction]:
        """
        Fetches the latest transactions from GoCardless bank accounts and applies any user filters.
        """
        transactions = []

        for t in api_transactions:
            if t.transactionId is None:
                continue

            amount = float(t.transactionAmount.amount)

            # Transaction descriptions are weird...
            description: str | None = None
            if t.remittanceInformationUnstructured is not None:
                description = t.remittanceInformationUnstructured
            elif t.remittanceInformationUnstructuredArray is not None:
                description = " ".join(t.remittanceInformationUnstructuredArray)

            # Convert date to datetime object
            # Some transactions have valueDateTime, some have valueDate
            if t.valueDateTime is not None:
                date = dt.datetime.fromisoformat(t.valueDateTime)
            elif t.valueDate is not None:
                date = dt.datetime.strptime(t.valueDate, "%Y-%m-%d").replace(
                    hour=0, minute=0, second=0
                )
            else:
                date = dt.datetime.max

            counterparty = t.debtorName if t.debtorName else t.creditorName

            encrypted_amount = self.encryption_service.encrypt_data(str(amount))
            encrypted_description = self.encryption_service.encrypt_data(
                description if description is not None else ""
            )
            encrypted_counterparty = self.encryption_service.encrypt_data(
                counterparty if counterparty is not None else ""
            )

            new_t = BankTransaction(
                user_id=self.user.id,
                transaction_id=t.transactionId,
                account_id=account.id,
                date=date,
                amount=encrypted_amount,
                description=encrypted_description,
                counterparty=encrypted_counterparty,
            )
            transactions.append(new_t)

        return transactions

    def fetch_new_transactions(self, account: BankAccount) -> None:
        api_transactions = self.gocardless_api.get_account_transactions(
            self.encryption_service.decrypt_data(account.account_id),
            account.last_synced.strftime("%Y-%m-%d"),
        )
        transactions = self._parse_transactions(account, api_transactions.booked)
        account.last_synced = dt.datetime.now()

        self.session.add(transactions)
        self.session.commit()
