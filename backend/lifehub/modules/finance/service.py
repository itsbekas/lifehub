import datetime as dt
import uuid
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session

from lifehub.core.common.base.service.user import BaseUserService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.security.encryption import EncryptionService
from lifehub.core.user.schema import User
from lifehub.providers.gocardless.api_client import GoCardlessAPIClient
from lifehub.providers.trading212.api_client import Trading212APIClient
from lifehub.providers.trading212.repository.t212_dividend import T212DividendRepository
from lifehub.providers.trading212.repository.t212_order import T212OrderRepository
from lifehub.providers.trading212.repository.t212_transaction import (
    T212TransactionRepository,
)

from .models import (
    BankBalanceResponse,
    BankInstitutionResponse,
    BankTransactionFilterRequest,
    BankTransactionFilterResponse,
    BankTransactionResponse,
    BudgetCategoryResponse,
    BudgetSubCategoryResponse,
    T212TransactionResponse,
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

    def fetch_t212_balance(self) -> BankBalanceResponse:
        """
        Fetches the latest balance from Trading212 and stores it in the database.
        If the local balance is less than an hour old, it will be returned instead.
        """
        t212_api = Trading212APIClient(self.user, self.session)
        balance_repo = AccountBalanceRepository(self.user, self.session)

        db_balance = balance_repo.get_by_account_id("trading212")

        if db_balance is not None and not db_balance.older_than(hours=1):
            # Local balance is updated
            balance = db_balance
        else:
            api_balance = t212_api.get_account_cash()
            if db_balance is None:
                balance = AccountBalance(
                    user_id=self.user.id,
                    account_id="trading212",
                    amount=api_balance.free,
                )
                balance_repo.add(balance)
            else:
                db_balance.amount = Decimal(api_balance.free)
                balance = db_balance

        res = BankBalanceResponse(
            bank="trading212", account_id="trading212", balance=float(balance.amount)
        )
        self.session.commit()
        return res

    def fetch_gocardless_balance(self, account: BankAccount) -> BankBalanceResponse:
        """
        Fetches the latest balance from GoCardless and stores it in the database.
        If the local balance is less than 6 hours old, it will be returned instead,
        since the API only allows 4 requests per day.
        """
        gc_api = GoCardlessAPIClient(self.user, self.session)
        balance_repo = AccountBalanceRepository(self.user, self.session)

        db_balance = balance_repo.get_by_account_id(account.id)

        if db_balance is not None and not db_balance.older_than(hours=6):
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
            bank=account.institution_id,
            account_id=str(account.id),
            balance=balance_amount,
        )
        self.session.commit()
        return res

    def get_t212_history(self) -> list[T212TransactionResponse]:
        transactions = T212TransactionRepository(self.user, self.session).get_all()
        orders = T212OrderRepository(self.user, self.session).get_all()
        dividends = T212DividendRepository(self.user, self.session).get_all()

        history = []

        for transaction in transactions:
            history.append(
                T212TransactionResponse(
                    timestamp=transaction.timestamp,
                    amount=float(transaction.amount),
                    type="transaction",
                    ticker=None,
                )
            )

        for order in orders:
            history.append(
                T212TransactionResponse(
                    timestamp=order.timestamp,
                    amount=float(order.quantity * order.price),
                    type="order",
                    ticker=order.ticker,
                )
            )

        for dividend in dividends:
            history.append(
                T212TransactionResponse(
                    timestamp=dividend.timestamp,
                    amount=float(dividend.amount),
                    type="dividend",
                    ticker=dividend.ticker,
                )
            )

        return history

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
                    institution_id=requisition.institution_id,
                    requisition_id=ref,
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
            match account.institution_id:
                case "trading212":
                    balance = self.fetch_t212_balance()
                case _:
                    balance = self.fetch_gocardless_balance(account)
            balances.append(balance)

        return balances

    def get_institutions(self) -> list[BankInstitutionResponse]:
        """
        Fetches the available institutions for bank connections.
        """
        gc_api = GoCardlessAPIClient(self.user, self.session)
        return [
            BankInstitutionResponse(
                id=inst.id,
                name=inst.name,
                logo=inst.logo,
            )
            for inst in gc_api.get_institutions()
        ]

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

    def get_bank_transactions(self) -> list[BankTransactionResponse]:
        """
        Fetches the latest transactions from the bank accounts and applies any user filters.
        """
        gc_api = GoCardlessAPIClient(self.user, self.session)
        bank_account_repo = BankAccountRepository(self.user, self.session)
        bank_transaction_repo = BankTransactionRepository(self.user, self.session)

        transactions = []

        for account in bank_account_repo.get_all():
            # If the last sync was less than 6 hours ago, get the transactions from the database
            if account.last_synced > dt.datetime.now() - dt.timedelta(hours=6):
                for synced_t in bank_transaction_repo.get_by_account_id(account.id):
                    synced_description = self.e.decrypt_data(
                        synced_t.user_description
                    ) or self.e.decrypt_data(synced_t.description)

                    transactions.append(
                        BankTransactionResponse(
                            id=str(synced_t.id),
                            account_id=str(synced_t.account.id),
                            amount=float(self.e.decrypt_data(synced_t.amount)),
                            date=synced_t.date,
                            description=synced_description,
                            counterparty=self.e.decrypt_data(synced_t.counterparty),
                            subcategory_id=str(synced_t.subcategory_id),
                        )
                    )
                continue

            account_id = self.encryption_service.decrypt_data(account.account_id)
            account_transactions = gc_api.get_account_transactions(account_id).booked

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
                        description = " ".join(
                            api_t.remittanceInformationUnstructuredArray
                        )

                    user_description = None

                    # Convert date to datetime object
                    # Some transactions have valueDateTime, some have valueDate
                    if api_t.valueDateTime is not None:
                        date = dt.datetime.fromisoformat(api_t.valueDateTime)
                    elif api_t.valueDate is not None:
                        date = dt.datetime.strptime(
                            api_t.valueDate, "%Y-%m-%d"
                        ).replace(hour=0, minute=0, second=0)
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
                else:
                    amount = float(self.e.decrypt_data(db_t.amount))
                    description = self.e.decrypt_data(db_t.description)
                    counterparty = self.e.decrypt_data(db_t.counterparty)
                    user_description = self.e.decrypt_data(db_t.user_description)

                # Apply filters to update subcategory_id and user_description
                self.apply_filters_to_transaction(db_t)

                transactions.append(
                    BankTransactionResponse(
                        id=str(db_t.id),
                        account_id=str(account.id),
                        amount=amount,
                        date=db_t.date,
                        description=user_description or description,
                        counterparty=counterparty,
                        subcategory_id=str(db_t.subcategory_id)
                        if db_t.subcategory_id
                        else None,
                    )
                )

            account.last_synced = dt.datetime.now()

        self.session.commit()

        return transactions

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
                        name=subcategory.name,
                        category_id=str(category.id),
                        category_name=category.name,
                        budgeted=budgeted,
                        spent=spent,
                        available=available,
                    )
                )
            categories.append(
                BudgetCategoryResponse(
                    id=str(category.id), name=category.name, subcategories=subcategories
                )
            )
        return categories

    def create_budget_category(self, name: str) -> BudgetCategoryResponse:
        """
        Creates a new budget category.
        """
        category = BudgetCategory(
            user_id=self.user.id,
            name=name,
        )
        self.user.budget_categories.append(category)
        self.session.commit()
        return BudgetCategoryResponse(
            id=str(category.id), name=category.name, subcategories=[]
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
                    name=subcategory.name,
                    category_id=str(category.id),
                    category_name=category.name,
                    budgeted=budgeted,
                    spent=spent,
                    available=available,
                )
            )

        return BudgetCategoryResponse(
            id=str(category.id), name=category.name, subcategories=subcategories
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
        category.name = name
        self.session.commit()
        return BudgetCategoryResponse(
            id=str(category.id), name=category.name, subcategories=[]
        )

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
                    name=subcategory.name,
                    category_id=str(category.id),
                    category_name=category.name,
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
            name=name,
            amount=Decimal(amount),
        )
        category.subcategories.append(subcategory)
        self.session.commit()

        # Fetch budgeted amount
        budgeted = float(subcategory.amount)

        # Initially, there are no transactions, so spent is 0 and available equals the budgeted amount
        spent = 0.0
        available = budgeted - spent

        return BudgetSubCategoryResponse(
            id=str(subcategory.id),
            name=subcategory.name,
            category_id=str(category.id),
            category_name=category.name,
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
        subcategory.name = name
        subcategory.amount = Decimal(amount)
        self.session.commit()

        budgeted, spent, available = self._get_budget_status(subcategory.id)

        return BudgetSubCategoryResponse(
            id=str(subcategory.id),
            name=subcategory.name,
            category_id=str(subcategory.category_id),
            category_name=subcategory.category.name,
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
        budgeted = float(subcategory.amount)

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
        new_matches = set(data.matches)

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
