import datetime as dt
import uuid
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session

from lifehub.config.constants import cfg
from lifehub.core.common.base.pagination import PaginatedResponse
from lifehub.core.common.base.service.user import BaseUserService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.provider.repository.provider import ProviderRepository
from lifehub.core.security.encryption import EncryptionService
from lifehub.core.user.schema import User
from lifehub.providers.gocardless.api_client import GoCardlessAPIClient
from lifehub.providers.trading212.api_client import Trading212APIClient

from .models import (
    BankBalanceResponse,
    BankInstitutionResponse,
    BankTransactionFilterRequest,
    BankTransactionFilterResponse,
    BankTransactionResponse,
    BudgetCategoryResponse,
    BudgetSubCategoryResponse,
    CountryResponse,
)
from .repository import (
    AccountBalanceRepository,
    BankAccountRepository,
    BankTransactionFilterRepository,
    BankTransactionRepository,
    BudgetCategoryRepository,
    BudgetSubCategoryRepository,
)
from .schema import (
    AccountBalance,
    BankAccount,
    BankTransaction,
    BankTransactionFilter,
    BankTransactionFilterMatch,
    BudgetCategory,
    BudgetSubCategory,
)


class FinanceServiceException(ServiceException):
    def __init__(self, status_code: int, message: str):
        super().__init__("Finance", status_code, message)


class FinanceService(BaseUserService):
    def __init__(self, session: Session, user: User):
        super().__init__(session, user)
        self.encryption_service = EncryptionService(session, user)
        self.e = self.encryption_service

    def _fetch_new_balance(self, account: BankAccount) -> BankBalanceResponse:
        """
        Fetches the latest balance from bank accounts based on their provider.
        """
        institution_id = self.encryption_service.decrypt_data(account.institution_id)
        match institution_id:
            case "trading212":
                return self._fetch_trading212_balance(account)
            case _:
                return self._fetch_gocardless_balance(account)

    def _fetch_trading212_balance(self, account: BankAccount) -> BankBalanceResponse:
        """
        Fetches the latest balance from Trading212 and stores it in the database.
        If the local balance is less than an hour old, it will be returned instead.
        """
        t212_api = Trading212APIClient(self.user, self.session)
        balance_repo = AccountBalanceRepository(self.user, self.session)

        db_balance = balance_repo.get_by_account_id(account.id)

        if db_balance is not None and not account.synced_before(hours=1):
            # Local balance is updated
            balance = db_balance
            balance_amount = float(self.encryption_service.decrypt_data(balance.amount))
        else:
            api_balance = t212_api.get_account_cash()
            if api_balance is None:
                raise FinanceServiceException(500, "Balance not found")

            balance_amount = float(api_balance.free)
            encrypted_balance = self.encryption_service.encrypt_data(
                str(api_balance.free)
            )

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

        res = BankBalanceResponse(
            bank="trading212",
            account_id=str(account.id),
            balance=balance_amount,
        )
        self.session.commit()
        return res

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

        res = BankBalanceResponse(
            bank=self.e.decrypt_data(account.institution_id),
            account_id=str(account.id),
            balance=balance_amount,
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
                    institution_id=self.e.encrypt_data(requisition.institution_id),
                    requisition_id=self.e.encrypt_data(ref),
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

        return balances

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

    def apply_filters_to_transaction(self, transaction: BankTransaction) -> None:
        """
        Apply user's filters to a given transaction. If any match rules of a filter are met,
        update the transaction's subcategory_id and user_description.
        """
        bank_transaction_filters_repo = BankTransactionFilterRepository(
            self.user, self.session
        )
        filters = bank_transaction_filters_repo.get_all()

        for filter in filters:
            for match_rule in filter.matches:
                if (
                    match_rule.match_string.lower() in transaction.description.lower()
                    if transaction.description
                    else False
                ) or (
                    match_rule.match_string.lower() in transaction.counterparty.lower()
                    if transaction.counterparty
                    else False
                ):
                    # Update the transaction's subcategory_id and user_description
                    transaction.subcategory_id = filter.subcategory_id
                    transaction.user_description = filter.description
                    break  # Stop checking more match rules for this filter

        self.session.commit()

    def _fetch_new_transactions(self, account: BankAccount) -> None:
        """
        Fetches the latest transactions from bank accounts based on their provider.
        """
        institution_id = self.encryption_service.decrypt_data(account.institution_id)
        match institution_id:
            case "trading212":
                self._fetch_trading212_transactions(account)
            case _:
                self._fetch_gocardless_transactions(account)

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

                # Apply filters to update subcategory_id and user_description
                self.apply_filters_to_transaction(db_t)

        account.last_synced = dt.datetime.now()

        self.session.commit()

    def _fetch_trading212_transactions(self, account: BankAccount) -> None:
        t212_api = Trading212APIClient(self.user, self.session)

        to_date = dt.datetime.now() - dt.timedelta(minutes=30)
        from_date = to_date - dt.timedelta(weeks=52)
        res = t212_api.export_csv(
            include_dividends=True,
            include_interest=True,
            include_orders=True,
            include_transactions=True,
            from_date=from_date,
            to_date=to_date,
        )

        report_id = res.reportId

    def get_bank_transactions(
        self, request: BankTransactionFilterRequest
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
                self._fetch_new_transactions(account)

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
                amount=float(self.e.decrypt_data(transaction.amount)),
                date=transaction.date,
                description=self.e.decrypt_data(transaction.user_description)
                or self.e.decrypt_data(transaction.description),
                counterparty=self.e.decrypt_data(transaction.counterparty),
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
            db_t.user_description = self.e.encrypt_data(user_description)
        if subcategory_id is not None:
            db_t.subcategory_id = uuid.UUID(subcategory_id)
        if amount is not None:
            db_t.amount = self.e.encrypt_data(str(amount))

        self.session.commit()

        description = (
            user_description
            or self.e.decrypt_data(db_t.user_description)
            or self.e.decrypt_data(db_t.description)
        )
        counterparty = self.e.decrypt_data(db_t.counterparty)
        amount = amount or float(self.e.decrypt_data(db_t.amount))

        return BankTransactionResponse(
            id=str(db_t.id),
            account_id=str(db_t.account.id),
            amount=amount,
            date=db_t.date,
            description=description,
            counterparty=counterparty,
            subcategory_id=str(db_t.subcategory_id) if db_t.subcategory_id else None,
        )

    def get_budget_categories(self) -> list[BudgetCategoryResponse]:
        """
        Fetches the budget categories and subcategories, dynamically calculating the budgeted, spent, and available amounts.
        """
        categories = []
        for category in self.user.budget_categories:
            subcategories = []
            for subcategory in category.subcategories:
                budgeted, spent, available = self._get_budget_status(subcategory.id)

                subcategories.append(
                    BudgetSubCategoryResponse(
                        id=str(subcategory.id),
                        name=self.e.decrypt_data(subcategory.name),
                        category_id=str(category.id),
                        category_name=self.e.decrypt_data(category.name),
                        budgeted=budgeted,
                        spent=spent,
                        available=available,
                    )
                )
            categories.append(
                BudgetCategoryResponse(
                    id=str(category.id),
                    name=self.e.decrypt_data(category.name),
                    subcategories=subcategories,
                )
            )
        return categories

    def create_budget_category(self, name: str) -> BudgetCategoryResponse:
        """
        Creates a new budget category.
        """
        category = BudgetCategory(
            user_id=self.user.id,
            name=self.e.encrypt_data(name),
        )
        self.user.budget_categories.append(category)
        self.session.commit()
        return BudgetCategoryResponse(
            id=str(category.id),
            name=self.e.decrypt_data(category.name),
            subcategories=[],
        )

    def get_budget_category(self, category_id: uuid.UUID) -> BudgetCategoryResponse:
        """
        Fetches a budget category by ID, dynamically calculating the budgeted, spent, and available amounts for each subcategory.
        """
        category = BudgetCategoryRepository(self.user, self.session).get_by_id(
            category_id
        )
        if category is None:
            raise FinanceServiceException(404, "Category not found")

        subcategories = []
        for subcategory in category.subcategories:
            budgeted, spent, available = self._get_budget_status(subcategory.id)

            subcategories.append(
                BudgetSubCategoryResponse(
                    id=str(subcategory.id),
                    name=self.e.decrypt_data(subcategory.name),
                    category_id=str(category.id),
                    category_name=self.e.decrypt_data(category.name),
                    budgeted=budgeted,
                    spent=spent,
                    available=available,
                )
            )

        return BudgetCategoryResponse(
            id=str(category.id),
            name=self.e.decrypt_data(category.name),
            subcategories=subcategories,
        )

    def update_budget_category(
        self, category_id: uuid.UUID, name: str
    ) -> BudgetCategoryResponse:
        """
        Updates a budget category by ID.
        """
        category = BudgetCategoryRepository(self.user, self.session).get_by_id(
            category_id
        )
        if category is None:
            raise FinanceServiceException(404, "Category not found")
        category.name = self.e.encrypt_data(name)
        self.session.commit()
        return BudgetCategoryResponse(id=str(category.id), name=name, subcategories=[])

    def delete_budget_category(self, category_id: uuid.UUID) -> None:
        """
        Deletes a budget category by ID.
        """
        category = BudgetCategoryRepository(self.user, self.session).get_by_id(
            category_id
        )
        if category is None:
            raise FinanceServiceException(404, "Category not found")
        self.session.delete(category)
        self.session.commit()

    def get_budget_subcategories(
        self, category_id: uuid.UUID
    ) -> list[BudgetSubCategoryResponse]:
        """
        Fetches the subcategories of a budget category, dynamically calculating the budgeted, spent, and available amounts.
        """
        category = BudgetCategoryRepository(self.user, self.session).get_by_id(
            category_id
        )
        if category is None:
            raise FinanceServiceException(404, "Category not found")

        subcategories = []
        for subcategory in category.subcategories:
            budgeted, spent, available = self._get_budget_status(subcategory.id)

            subcategories.append(
                BudgetSubCategoryResponse(
                    id=str(subcategory.id),
                    name=self.e.decrypt_data(subcategory.name),
                    category_id=str(category.id),
                    category_name=self.e.decrypt_data(category.name),
                    budgeted=budgeted,
                    spent=spent,
                    available=available,
                )
            )
        return subcategories

    def create_budget_subcategory(
        self, category_id: uuid.UUID, name: str, amount: float
    ) -> BudgetSubCategoryResponse:
        """
        Creates a new budget subcategory with the specified budgeted amount.
        """
        category = BudgetCategoryRepository(self.user, self.session).get_by_id(
            category_id
        )
        if category is None:
            raise FinanceServiceException(404, "Category not found")

        subcategory = BudgetSubCategory(
            user_id=self.user.id,
            category_id=category.id,
            name=self.e.encrypt_data(name),
            amount=self.e.encrypt_data(str(Decimal(amount))),
        )
        category.subcategories.append(subcategory)
        self.session.commit()

        # Fetch budgeted amount
        budgeted = float(self.e.decrypt_data(subcategory.amount))

        # Initially, there are no transactions, so spent is 0 and available equals the budgeted amount
        spent = 0.0
        available = budgeted - spent

        return BudgetSubCategoryResponse(
            id=str(subcategory.id),
            name=self.e.decrypt_data(subcategory.name),
            category_id=str(category.id),
            category_name=self.e.decrypt_data(category.name),
            budgeted=budgeted,
            spent=spent,
            available=available,
        )

    def update_budget_subcategory(
        self, subcategory_id: uuid.UUID, name: str, amount: float
    ) -> BudgetSubCategoryResponse:
        """
        Updates a budget subcategory by ID.
        """
        subcategory = BudgetSubCategoryRepository(self.user, self.session).get_by_id(
            subcategory_id
        )
        if subcategory is None:
            raise FinanceServiceException(404, "Subcategory not found")
        subcategory.name = self.e.encrypt_data(name)
        subcategory.amount = self.e.encrypt_data(str(Decimal(amount)))
        self.session.commit()

        budgeted, spent, available = self._get_budget_status(subcategory.id)

        return BudgetSubCategoryResponse(
            id=str(subcategory.id),
            name=self.e.decrypt_data(subcategory.name),
            category_id=str(subcategory.category_id),
            category_name=self.e.decrypt_data(subcategory.category.name),
            budgeted=budgeted,
            spent=spent,
            available=available,
        )

    def delete_budget_subcategory(self, subcategory_id: uuid.UUID) -> None:
        """
        Deletes a budget subcategory by ID.
        """
        subcategory = BudgetSubCategoryRepository(self.user, self.session).get_by_id(
            subcategory_id
        )
        if subcategory is None:
            raise FinanceServiceException(404, "Subcategory not found")
        self.session.delete(subcategory)
        self.session.commit()

    def get_transactions_for_current_month(self) -> list[BankTransactionResponse]:
        """
        Fetches the user's transactions for the current month.
        """
        bank_transaction_repo = BankTransactionRepository(self.user, self.session)
        start_of_month = dt.datetime.now().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        transactions = bank_transaction_repo.get_transactions_since(start_of_month)

        return [
            BankTransactionResponse(
                id=str(transaction.id),
                account_id=str(transaction.account.id),
                amount=float(transaction.amount),
                date=transaction.date,
                description=transaction.description,
                counterparty=transaction.counterparty,
                subcategory_id=str(transaction.subcategory_id)
                if transaction.subcategory_id
                else None,
                user_description=transaction.user_description,
            )
            for transaction in transactions
        ]

    def _get_current_month_transactions_by_subcategory(
        self, subcategory_id: uuid.UUID
    ) -> list[BankTransaction]:
        """
        Fetches all transactions related to a specific subcategory for the current month.
        """
        bank_transaction_repo = BankTransactionRepository(self.user, self.session)
        start_of_month = dt.datetime.now().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        return bank_transaction_repo.get_transactions_since(
            start_of_month, subcategory_id=subcategory_id
        )

    def _get_budget_status(
        self, subcategory_id: uuid.UUID
    ) -> tuple[float, float, float]:
        """
        Fetches the budgeted, spent, and available amounts for a specific subcategory.
        """
        subcategory = BudgetSubCategoryRepository(self.user, self.session).get_by_id(
            subcategory_id
        )

        if subcategory is None:
            raise FinanceServiceException(404, "Subcategory not found")

        # Fetch budgeted amount
        budgeted = float(self.e.decrypt_data(subcategory.amount))

        # Calculate spent amount
        transactions = self._get_current_month_transactions_by_subcategory(
            subcategory_id
        )
        spent = -float(
            sum(
                float(self.encryption_service.decrypt_data(transaction.amount))
                for transaction in transactions
            )
        )

        # Calculate available amount
        available = budgeted - spent
        return round(budgeted, 2), round(spent, 2), round(available, 2)

    def get_bank_transactions_filters(self) -> list[BankTransactionFilterResponse]:
        bank_transaction_filters_repo = BankTransactionFilterRepository(
            self.user, self.session
        )
        return [
            BankTransactionFilterResponse(
                id=str(filter.id),
                description=filter.description,
                subcategory_id=str(filter.subcategory_id),
                matches=[match.match_string for match in filter.matches],
            )
            for filter in bank_transaction_filters_repo.get_all()
        ]

    def create_bank_transactions_filter(
        self, data: BankTransactionFilterRequest
    ) -> BankTransactionFilterResponse:
        bank_transaction_filters_repo = BankTransactionFilterRepository(
            self.user, self.session
        )
        filter = BankTransactionFilter(
            user_id=self.user.id,
            description=data.description if data.description else None,
            subcategory_id=uuid.UUID(data.subcategory_id)
            if data.subcategory_id
            else None,
            matches=[],
        )

        # Handle the case where matches is None
        if data.matches is not None:
            filter.matches = [
                BankTransactionFilterMatch(filter_id=filter.id, match_string=match)
                for match in data.matches
            ]

        bank_transaction_filters_repo.add(filter)

        self.session.commit()
        return BankTransactionFilterResponse(
            id=str(filter.id),
            description=filter.description,
            subcategory_id=str(filter.subcategory_id)
            if filter.subcategory_id
            else None,
            matches=[match.match_string for match in filter.matches],
        )

    def update_bank_transactions_filter(
        self, filter_id: uuid.UUID, data: BankTransactionFilterRequest
    ) -> BankTransactionFilterResponse:
        bank_transaction_filters_repo = BankTransactionFilterRepository(
            self.user, self.session
        )
        filter = bank_transaction_filters_repo.get_by_id(filter_id)
        if filter is None:
            raise FinanceServiceException(404, "Filter not found")
        filter.description = (
            data.description if data.description else filter.description
        )
        filter.subcategory_id = (
            uuid.UUID(data.subcategory_id)
            if data.subcategory_id
            else filter.subcategory_id
        )

        # Update matches explicitly
        existing_matches = {match.match_string for match in filter.matches}
        new_matches = set(data.matches or [])

        # Add new matches
        for match_string in new_matches - existing_matches:
            filter.matches.append(
                BankTransactionFilterMatch(
                    filter_id=filter.id, match_string=match_string
                )
            )

        # Remove old matches explicitly
        matches_to_remove = [
            match for match in filter.matches if match.match_string not in new_matches
        ]
        for match in matches_to_remove:
            self.session.delete(match)  # Explicitly delete match from the session

        self.session.commit()

        return BankTransactionFilterResponse(
            id=str(filter.id),
            description=filter.description,
            subcategory_id=str(filter.subcategory_id)
            if filter.subcategory_id
            else None,
            matches=[match.match_string for match in filter.matches],
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
        bank_account_repo.add(
            BankAccount(
                user_id=self.user.id,
                account_id=self.encryption_service.encrypt_data(""),
                institution_id=self.encryption_service.encrypt_data(bank_id),
                requisition_id=self.encryption_service.encrypt_data(""),
            )
        )

        self.session.commit()
