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
from lifehub.modules.finance.service.t212_service import Trading212Service
from lifehub.providers.gocardless.api_client import GoCardlessAPIClient

from ..models import (
    BankBalanceResponse,
    BankInstitutionResponse,
    BankTransactionResponse,
    CountryResponse,
    GetBankTransactionsRequest,
)
from ..repository import (
    AccountBalanceRepository,
    BankAccountRepository,
    BankTransactionRepository,
)
from ..schema import AccountBalance, BankAccount, BankTransaction


class FinanceServiceException(ServiceException):
    def __init__(self, status_code: int, message: str):
        super().__init__("Finance", status_code, message)


class FinanceService(BaseUserService):
    _encryption_service: EncryptionService | None = None
    _trading212_service: Trading212Service | None = None
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
    def filter_service(self) -> FilterService:
        if self._filter_service is None:
            self._filter_service = FilterService(self.session, self.user)
        return self._filter_service

    def _fetch_new_balance(self, account: BankAccount) -> BankBalanceResponse:
        """
        Fetches the latest balance from bank accounts based on their provider.
        """
        institution_id = self.encryption_service.decrypt_data(account.institution_id)
        match institution_id:
            case "trading212":
                return self.trading212_service.fetch_balance(account)
            case _:
                return self._fetch_gocardless_balance(account)

    def _fetch_gocardless_balance(self, account: BankAccount) -> BankBalanceResponse:
        """
        Fetches the latest balance from GoCardless and stores it in the database.
        If the local balance is less than 6 hours old, it will be returned instead,
        since the API only allows 4 requests per day.
        """
        gc_api = GoCardlessAPIClient(self.user, self.session)
        balance_repo = AccountBalanceRepository(self.user, self.session)

        db_balance = balance_repo.get_by_account_id(account.id)

        if db_balance is not None and not account.synced_before(hours=6):
            # Local balance is updated
            balance = db_balance
            balance_amount = float(self.encryption_service.decrypt_data(balance.amount))
        else:
            account_id = self.encryption_service.decrypt_data(account.account_id)
            api_balance = gc_api.get_account_balances(account_id).available_amount

            if api_balance is None:
                # return seconds left until balance is available (check error message)
                raise FinanceServiceException(500, "Balance not found")

            balance_amount = float(api_balance)
            encrypted_balance = self.encryption_service.encrypt_data(api_balance)

            if db_balance is None:
                balance = AccountBalance(
                    user_id=self.user.id,
                    account_id=account.id,
                    amount=encrypted_balance,
                )
                balance_repo.add(balance)
            else:
                db_balance.amount = encrypted_balance
                balance = db_balance

        # Calculate monthly summary data
        monthly_income = 0.0
        monthly_expenses = 0.0
        monthly_last_updated = None

        if db_balance is not None:
            if db_balance.monthly_income is not None:
                monthly_income = float(
                    self.encryption_service.decrypt_data(db_balance.monthly_income)
                )
            if db_balance.monthly_expenses is not None:
                monthly_expenses = float(
                    self.encryption_service.decrypt_data(db_balance.monthly_expenses)
                )
            monthly_last_updated = db_balance.monthly_last_updated

        # If monthly data is missing or outdated, update it
        now = dt.datetime.now()
        if monthly_last_updated is None or (now - monthly_last_updated).days > 0:
            # Get the current month's transactions
            start_of_month = dt.datetime(now.year, now.month, 1)
            bank_transaction_repo = BankTransactionRepository(self.user, self.session)
            transactions = bank_transaction_repo.get_transactions_since(start_of_month)

            # Calculate income and expenses
            monthly_income = 0.0
            monthly_expenses = 0.0

            for transaction in transactions:
                amount = float(self.encryption_service.decrypt_data(transaction.amount))
                if amount > 0:
                    monthly_income += amount
                else:
                    monthly_expenses += abs(amount)

            # Update the account balance with monthly summary
            if db_balance is not None:
                db_balance.monthly_income = self.encryption_service.encrypt_data(
                    str(monthly_income)
                )
                db_balance.monthly_expenses = self.encryption_service.encrypt_data(
                    str(monthly_expenses)
                )
                db_balance.monthly_last_updated = now
                monthly_last_updated = now

        res = BankBalanceResponse(
            bank=self.encryption_service.decrypt_data(account.institution_id),
            account_id=str(account.id),
            balance=balance_amount,
            monthly_income=monthly_income,
            monthly_expenses=monthly_expenses,
            monthly_last_updated=monthly_last_updated,
        )
        self.session.commit()
        return res

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

    def get_bank_login(self, bank_id: str) -> str:
        api = GoCardlessAPIClient(self.user, self.session)
        return api.create_requisition(bank_id).link

    def confirm_bank_login(self, ref: str) -> None:
        api = GoCardlessAPIClient(self.user, self.session)
        requisition = api.get_requisition(ref)
        bank_account_repo = BankAccountRepository(self.user, self.session)
        for account_id in requisition.accounts:
            encrypted_account_id = self.encryption_service.encrypt_data(account_id)
            bank_account_repo.add(
                BankAccount(
                    user_id=self.user.id,
                    account_id=encrypted_account_id,
                    institution_id=self.encryption_service.encrypt_data(
                        requisition.institution_id
                    ),
                    requisition_id=self.encryption_service.encrypt_data(ref),
                )
            )

        self.session.commit()

    def get_bank_balances(self) -> list[BankBalanceResponse]:
        """
        Fetches the latest balances from the bank accounts.
        """
        bank_account_repo = BankAccountRepository(self.user, self.session)
        balances = []

        for account in bank_account_repo.get_all():
            balance = self._fetch_new_balance(account)
            balances.append(balance)

            # Update monthly summary when fetching balances
            self._update_monthly_summary(account)

        return balances

    def _update_monthly_summary(self, account: BankAccount) -> None:
        """
        Calculates and updates the monthly summary for an account.
        """
        # Get the current month's transactions
        now = dt.datetime.now()
        start_of_month = dt.datetime(now.year, now.month, 1)

        bank_transaction_repo = BankTransactionRepository(self.user, self.session)
        transactions = bank_transaction_repo.get_transactions_since(start_of_month)

        # Calculate income and expenses
        income = 0.0
        expenses = 0.0

        for transaction in transactions:
            amount = float(self.encryption_service.decrypt_data(transaction.amount))
            if amount > 0:
                income += amount
            else:
                expenses += abs(amount)

        # Update the account balance with monthly summary
        balance_repo = AccountBalanceRepository(self.user, self.session)
        db_balance = balance_repo.get_by_account_id(account.id)

        if db_balance is not None:
            db_balance.monthly_income = self.encryption_service.encrypt_data(
                str(income)
            )
            db_balance.monthly_expenses = self.encryption_service.encrypt_data(
                str(expenses)
            )
            db_balance.monthly_last_updated = dt.datetime.now()

        self.session.commit()

    def get_institutions(self, country: str = "PT") -> list[BankInstitutionResponse]:
        """
        Fetches the available institutions for bank connections for a specific country.
        """
        gc_api = GoCardlessAPIClient(self.user, self.session)
        res = []

        for inst in gc_api.get_institutions(country):
            res.append(
                BankInstitutionResponse(
                    id=inst.id,
                    type="oauth",
                    name=inst.name,
                    logo=inst.logo,
                )
            )

        res.append(
            BankInstitutionResponse(
                id="trading212",
                type="token",
                name="Trading212",
                logo="",
            )
        )

        res.sort(key=lambda x: x.name)

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

    def fetch_new_transactions(self, account: BankAccount) -> None:
        """
        Fetches the latest transactions from bank accounts based on their provider.
        """
        institution_id = self.encryption_service.decrypt_data(account.institution_id)
        match institution_id:
            case "trading212":
                self.trading212_service.fetch_new_transactions(account)
            case _:
                self._fetch_gocardless_transactions(account)

    def _update_monthly_summary_incremental(
        self, account: BankAccount, new_transactions: list[BankTransaction]
    ) -> None:
        """
        Incrementally updates the monthly summary for an account based on new transactions.

        If the last update was in the current month, it adds the new transactions to the existing totals.
        Otherwise, it performs a full recalculation.

        Args:
            account: The bank account to update
            new_transactions: List of newly added transactions
        """
        now = dt.datetime.now()
        start_of_month = dt.datetime(now.year, now.month, 1)

        # Get the account balance
        balance_repo = AccountBalanceRepository(self.user, self.session)
        db_balance = balance_repo.get_by_account_id(account.id)

        if db_balance is None:
            # No balance record exists yet, nothing to update
            return

        # Check if we have monthly data and if it was updated this month
        monthly_last_updated = db_balance.monthly_last_updated

        if (
            monthly_last_updated is not None
            and monthly_last_updated.year == now.year
            and monthly_last_updated.month == now.month
        ):
            # Last update was this month, we can do an incremental update

            # Get current monthly totals
            monthly_income = 0.0
            monthly_expenses = 0.0

            if db_balance.monthly_income is not None:
                monthly_income = float(
                    self.encryption_service.decrypt_data(db_balance.monthly_income)
                )
            if db_balance.monthly_expenses is not None:
                monthly_expenses = float(
                    self.encryption_service.decrypt_data(db_balance.monthly_expenses)
                )

            # Add new transactions from the current month
            for transaction in new_transactions:
                # Only include transactions from the current month
                if transaction.date and transaction.date >= start_of_month:
                    amount = float(
                        self.encryption_service.decrypt_data(transaction.amount)
                    )
                    if amount > 0:
                        monthly_income += amount
                    else:
                        monthly_expenses += abs(amount)

            # Update the account balance with the new totals
            db_balance.monthly_income = self.encryption_service.encrypt_data(
                str(monthly_income)
            )
            db_balance.monthly_expenses = self.encryption_service.encrypt_data(
                str(monthly_expenses)
            )
            db_balance.monthly_last_updated = now

        else:
            # Last update was in a different month or doesn't exist, do a full recalculation
            self._update_monthly_summary(account)

    def _fetch_gocardless_transactions(self, account: BankAccount) -> None:
        """
        Fetches the latest transactions from GoCardless bank accounts and applies any user filters.
        """
        gc_api = GoCardlessAPIClient(self.user, self.session)
        bank_transaction_repo = BankTransactionRepository(self.user, self.session)

        account_id = self.encryption_service.decrypt_data(account.account_id)
        last_sync = (
            None  # New accounts
            if account.last_synced == dt.datetime.min
            else (account.last_synced - dt.timedelta(weeks=2)).strftime("%Y-%m-%d")
        )
        account_transactions = gc_api.get_account_transactions(
            account_id, last_sync
        ).booked

        # Keep track of new transactions for incremental monthly summary update
        new_transactions = []

        for api_t in account_transactions:
            if api_t.transactionId is None:
                continue

            db_t = bank_transaction_repo.get_by_original_id(
                account.id, api_t.transactionId
            )

            if db_t is None:
                amount = float(api_t.transactionAmount.amount)

                # Transaction descriptions are weird...
                description: str | None = None
                if api_t.remittanceInformationUnstructured is not None:
                    description = api_t.remittanceInformationUnstructured
                elif api_t.remittanceInformationUnstructuredArray is not None:
                    description = " ".join(api_t.remittanceInformationUnstructuredArray)

                # Convert date to datetime object
                # Some transactions have valueDateTime, some have valueDate
                if api_t.valueDateTime is not None:
                    date = dt.datetime.fromisoformat(api_t.valueDateTime)
                elif api_t.valueDate is not None:
                    date = dt.datetime.strptime(api_t.valueDate, "%Y-%m-%d").replace(
                        hour=0, minute=0, second=0
                    )
                else:
                    date = dt.datetime.max

                counterparty = (
                    api_t.debtorName if api_t.debtorName else api_t.creditorName
                )

                encrypted_amount = self.encryption_service.encrypt_data(str(amount))
                encrypted_description = self.encryption_service.encrypt_data(
                    description if description is not None else ""
                )
                encrypted_counterparty = self.encryption_service.encrypt_data(
                    counterparty if counterparty is not None else ""
                )

                db_t = BankTransaction(
                    user_id=self.user.id,
                    transaction_id=api_t.transactionId,
                    account_id=account.id,
                    amount=encrypted_amount,
                    date=date,
                    description=encrypted_description,
                    counterparty=encrypted_counterparty,
                )
                bank_transaction_repo.add(db_t)
                new_transactions.append(db_t)

                # Apply filters to update subcategory_id and user_description
                self.filter_service.apply_filters_to_transaction(db_t)

        # Update the account's last synced timestamp
        account.last_synced = dt.datetime.now()

        # Incrementally update the monthly summary with the new transactions
        if new_transactions:
            self._update_monthly_summary_incremental(account, new_transactions)

        self.session.commit()

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
        bank_transaction_repo = BankTransactionRepository(self.user, self.session)

        # Sync transactions if needed
        for account in bank_account_repo.get_all():
            if account.synced_before(hours=6):
                self.fetch_new_transactions(account)

        # Get paginated transactions from repository
        paginated_transactions = bank_transaction_repo.get_paginated_transactions(
            request=request,
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
        bank_transaction_repo = BankTransactionRepository(self.user, self.session)
        db_t = bank_transaction_repo.get_by_id(transaction_id)

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
            institution_id=self.encryption_service.encrypt_data(bank_id),
            requisition_id=self.encryption_service.encrypt_data(""),
        )
        bank_account_repo.add(new_account)

        if bank_id == "trading212":
            self.trading212_service.fetch_all_transactions(new_account)

        self.session.commit()
