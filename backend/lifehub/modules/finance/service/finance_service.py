import datetime as dt
import uuid
from typing import Optional

from sqlalchemy.orm import Session

from lifehub.config.constants import cfg
from lifehub.core.common.base.pagination import PaginatedResponse
from lifehub.core.common.base.service.user import BaseUserService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.provider.repository.provider import ProviderRepository
from lifehub.core.security.encryption import EncryptionService
from lifehub.core.user.schema import User
from lifehub.modules.finance.service.filter_service import FilterService
from lifehub.modules.finance.service.gocardless_service import GoCardlessService
from lifehub.modules.finance.service.t212_service import Trading212Service

from ..models import (
    BankBalanceResponse,
    BankInstitutionResponse,
    BankMonthlySummaryCategoryResponse,
    BankMonthlySummaryResponse,
    BankTransactionResponse,
    CountryResponse,
    GetBankTransactionsRequest,
)
from ..repository import BankAccountRepository, BankTransactionRepository
from ..schema import AccountBalance, BankAccount


class FinanceServiceException(ServiceException):
    def __init__(self, status_code: int, message: str):
        super().__init__("Finance", status_code, message)


class FinanceService(BaseUserService):
    _encryption_service: EncryptionService | None = None
    _trading212_service: Trading212Service | None = None
    _gocardless_service: GoCardlessService | None = None
    _filter_service: FilterService | None = None

    def __init__(self, session: Session, user: User):
        super().__init__(session, user)

    @property
    def encryption_service(self) -> EncryptionService:
        if self._encryption_service is None:
            self._encryption_service = EncryptionService(self.session, self.user)
        return self._encryption_service

    @property
    def trading212_service(self) -> Trading212Service:
        if self._trading212_service is None:
            self._trading212_service = Trading212Service(self.session, self.user)
        return self._trading212_service

    @property
    def gocardless_service(self) -> GoCardlessService:
        if self._gocardless_service is None:
            self._gocardless_service = GoCardlessService(
                session=self.session, user=self.user
            )
        return self._gocardless_service

    @property
    def filter_service(self) -> FilterService:
        if self._filter_service is None:
            self._filter_service = FilterService(self.session, self.user)
        return self._filter_service

    def get_countries(self) -> list[CountryResponse]:
        """Returns a list of supported countries."""
        return [
            CountryResponse(name="Austria", code="AT"),
            CountryResponse(name="Belgium", code="BE"),
            CountryResponse(name="Bulgaria", code="BG"),
            CountryResponse(name="Croatia", code="HR"),
            CountryResponse(name="Cyprus", code="CY"),
            CountryResponse(name="Czech Republic", code="CZ"),
            CountryResponse(name="Denmark", code="DK"),
            CountryResponse(name="Estonia", code="EE"),
            CountryResponse(name="Finland", code="FI"),
            CountryResponse(name="France", code="FR"),
            CountryResponse(name="Germany", code="DE"),
            CountryResponse(name="Greece", code="GR"),
            CountryResponse(name="Hungary", code="HU"),
            CountryResponse(name="Iceland", code="IS"),
            CountryResponse(name="Ireland", code="IE"),
            CountryResponse(name="Italy", code="IT"),
            CountryResponse(name="Latvia", code="LV"),
            CountryResponse(name="Liechtenstein", code="LI"),
            CountryResponse(name="Lithuania", code="LT"),
            CountryResponse(name="Luxembourg", code="LU"),
            CountryResponse(name="Malta", code="MT"),
            CountryResponse(name="Netherlands", code="NL"),
            CountryResponse(name="Norway", code="NO"),
            CountryResponse(name="Poland", code="PL"),
            CountryResponse(name="Portugal", code="PT"),
            CountryResponse(name="Romania", code="RO"),
            CountryResponse(name="Slovakia", code="SK"),
            CountryResponse(name="Slovenia", code="SI"),
            CountryResponse(name="Spain", code="ES"),
            CountryResponse(name="Sweden", code="SE"),
            CountryResponse(name="United Kingdom", code="GB"),
        ]

    def get_institutions(self, country: str = "PT") -> list[BankInstitutionResponse]:
        """
        Fetches the available institutions for bank connections for a specific country.
        """
        res = []
        # GoCardless
        res.extend(self.gocardless_service.get_institutions(country))
        # Trading212
        res.append(
            BankInstitutionResponse(
                id="trading212", type="token", name="Trading212", logo=""
            )
        )

        res.sort(key=lambda x: x.name)
        # Development
        if cfg.ENVIRONMENT == "development":
            res.append(
                BankInstitutionResponse(
                    id="SANDBOXFINANCE_SFIN0000",
                    type="oauth",
                    name="Sandbox Finance",
                    logo="",
                )
            )

        return res

    def get_bank_login(self, bank_id: str) -> str:
        return self.gocardless_service.get_bank_login(bank_id)

    def confirm_bank_login(self, ref: str) -> None:
        self.gocardless_service.confirm_bank_login(ref)

    def _sync_balance(self, account: BankAccount) -> BankBalanceResponse:
        """
        Fetches the latest balance from GoCardless bank accounts.
        """
        balance = None
        institution_id = self.encryption_service.decrypt_data(account.institution_id)
        match institution_id:
            case "trading212":
                balance = self.trading212_service.fetch_balance()
            case _:
                balance = self.gocardless_service.fetch_balance(account)

        if balance is None:
            raise FinanceServiceException(500, "Balance not found")

        encrypted_balance = self.encryption_service.encrypt_data(str(balance))
        account.balance.amount = encrypted_balance
        account.balance.last_synced = dt.datetime.now()
        self.session.commit()

        return BankBalanceResponse(
            bank=institution_id, account_id=str(account.id), balance=balance
        )

    def get_bank_balances(self) -> list[BankBalanceResponse]:
        """
        Fetches the latest balances from the bank accounts.
        """
        bank_account_repo = BankAccountRepository(self.user, self.session)
        balances: list[BankBalanceResponse] = []

        for account in bank_account_repo.get_all():
            if account.balance.synced_before(hours=6):
                balances.append(self._sync_balance(account))
            else:
                balances.append(
                    BankBalanceResponse(
                        bank=self.encryption_service.decrypt_data(
                            account.institution_id
                        ),
                        account_id=str(account.id),
                        balance=float(
                            self.encryption_service.decrypt_data(account.balance.amount)
                        ),
                    )
                )
        return balances

    def get_monthly_summary(self) -> BankMonthlySummaryResponse:
        bank_transaction_repo = BankTransactionRepository(self.session)
        start_date = dt.datetime.now().replace(day=1, hour=0, minute=0, second=0)
        transactions = bank_transaction_repo.get_since(
            accounts=BankAccountRepository(self.user, self.session).get_all(),
            since=start_date,
        )
        income = 0.0
        expenses = 0.0
        categories = {}

        for t in transactions:
            amount = float(self.encryption_service.decrypt_data(t.amount))
            if amount >= 0:
                income += amount
            else:
                expenses += abs(amount)

            subcategory_id = str(t.subcategory_id) if t.subcategory_id else None
            if subcategory_id not in categories:
                categories[subcategory_id] = {
                    "budgeted": 0.0,
                    "spent": 0.0,
                }
            categories[subcategory_id]["spent"] += abs(amount)

        return BankMonthlySummaryResponse(
            income=income,
            expenses=expenses,
            categories=[
                BankMonthlySummaryCategoryResponse(
                    subcategory_id=subcat_id,
                    balance=cat_data["spent"],
                )
                for subcat_id, cat_data in categories.items()
                if subcat_id is not None
            ],
        )

    def _fetch_new_transactions(self, account: BankAccount) -> None:
        """
        Fetches the latest transactions from bank accounts based on their provider.
        """
        institution_id = self.encryption_service.decrypt_data(account.institution_id)
        match institution_id:
            case "trading212":
                self.trading212_service.fetch_new_transactions(account)
            case _:
                self.gocardless_service.fetch_new_transactions(account)

    def get_bank_transactions(
        self, request: GetBankTransactionsRequest
    ) -> PaginatedResponse[BankTransactionResponse]:
        """
        Fetches paginated transactions with optional filtering.

        Args:
            request: Pagination and filtering parameters

        Returns:
            Paginated response with transaction data
        """
        bank_account_repo = BankAccountRepository(self.user, self.session)
        bank_transaction_repo = BankTransactionRepository(self.session)

        user_accounts = bank_account_repo.get_all()

        # Sync transactions if needed
        for account in user_accounts:
            if account.synced_before(hours=6):
                self._fetch_new_transactions(account)

        # Get paginated transactions from repository
        paginated_transactions = bank_transaction_repo.get_paginated_transactions(
            request=request,
            accounts=user_accounts,
            subcategory_id=uuid.UUID(request.subcategory_id)
            if request.subcategory_id
            else None,
            description=request.description,
        )

        # Convert DB models to response models
        transaction_responses = [
            BankTransactionResponse(
                id=str(transaction.id),
                account_id=str(transaction.account_id),
                amount=float(self.encryption_service.decrypt_data(transaction.amount)),
                date=transaction.date,
                description=self.encryption_service.decrypt_data(
                    transaction.user_description
                )
                or self.encryption_service.decrypt_data(transaction.description),
                counterparty=self.encryption_service.decrypt_data(
                    transaction.counterparty
                ),
                subcategory_id=str(transaction.subcategory_id)
                if transaction.subcategory_id
                else None,
            )
            for transaction in paginated_transactions.items
        ]

        # Create a new PaginatedResponse with the converted items
        return PaginatedResponse(
            items=transaction_responses, pagination=paginated_transactions.pagination
        )

    def update_bank_transaction(
        self,
        account_id: uuid.UUID,
        transaction_id: uuid.UUID,
        user_description: Optional[str],
        subcategory_id: Optional[str],
        amount: Optional[float],
    ) -> BankTransactionResponse:
        """
        Updates a bank transaction with user description and subcategory.
        """
        bank_account = BankAccountRepository(self.user, self.session).get_by_id(
            account_id
        )
        if bank_account is None:
            raise FinanceServiceException(404, "Bank account not found")

        bank_transaction_repo = BankTransactionRepository(self.session)
        db_t = bank_transaction_repo.get_by_id(bank_account, transaction_id)

        if db_t is None:
            raise FinanceServiceException(404, "Transaction not found")
        if user_description is not None:
            db_t.user_description = self.encryption_service.encrypt_data(
                user_description
            )
        if subcategory_id is not None:
            db_t.subcategory_id = uuid.UUID(subcategory_id)
        if amount is not None:
            db_t.amount = self.encryption_service.encrypt_data(str(amount))

        self.session.commit()

        description = (
            user_description
            or self.encryption_service.decrypt_data(db_t.user_description)
            or self.encryption_service.decrypt_data(db_t.description)
        )
        counterparty = self.encryption_service.decrypt_data(db_t.counterparty)
        amount = amount or float(self.encryption_service.decrypt_data(db_t.amount))

        return BankTransactionResponse(
            id=str(db_t.id),
            account_id=str(db_t.account.id),
            amount=amount,
            date=db_t.date,
            description=description,
            counterparty=counterparty,
            subcategory_id=str(db_t.subcategory_id) if db_t.subcategory_id else None,
        )

    def add_bank_account(self, bank_id: str) -> None:
        # Verify user has the required provider
        provider_repo = ProviderRepository(self.session)
        provider = provider_repo.get_by_id(bank_id)  # Using bank_id as provider_id
        if provider is None:
            raise Exception(f"Provider {bank_id} not found")

        if provider not in self.user.providers:
            raise Exception(
                f"User does not have the required provider: {provider.name}"
            )

        bank_account_repo = BankAccountRepository(self.user, self.session)
        # Some fields are empty because I didn't feel like changing the db fields
        # to nullable (alembic wasn't cooperating either)
        # Either way, it ends up providing some obfuscation into the account type
        new_account = BankAccount(
            user_id=self.user.id,
            account_id=self.encryption_service.encrypt_data(""),
            last_synced=dt.datetime.now() - dt.timedelta(weeks=52),
            institution_id=self.encryption_service.encrypt_data(bank_id),
            requisition_id=self.encryption_service.encrypt_data(""),
        )
        bank_account_repo.add(new_account)
        self.session.flush()

        self.session.add(
            AccountBalance(
                account_id=new_account.id,
                amount=self.encryption_service.encrypt_data("0.0"),
                last_synced=dt.datetime.now() - dt.timedelta(weeks=1),
            )
        )

        self.session.commit()
