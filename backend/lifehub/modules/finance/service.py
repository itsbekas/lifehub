import datetime as dt
import uuid
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session

from lifehub.core.common.base.service.user import BaseUserService
from lifehub.core.common.exceptions import ServiceException
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
    BankTransactionResponse,
    BudgetCategoryResponse,
    BudgetSubCategoryResponse,
    T212TransactionResponse,
)
from .repository import (
    AccountBalanceRepository,
    BankAccountRepository,
    BankTransactionRepository,
)
from .schema import (
    AccountBalance,
    BankAccount,
    BankTransaction,
    BudgetCategory,
    BudgetSubCategory,
)


class FinanceServiceException(ServiceException):
    def __init__(self, status_code: int, message: str):
        super().__init__("Finance", status_code, message)


class FinanceService(BaseUserService):
    def __init__(self, session: Session, user: User):
        super().__init__(session, user)

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

    def fetch_gocardless_balance(
        self, institution_id: str, account_id: str
    ) -> BankBalanceResponse:
        """
        Fetches the latest balance from GoCardless and stores it in the database.
        If the local balance is less than 6 hours old, it will be returned instead,
        since the API only allows 4 requests per day.
        """
        gc_api = GoCardlessAPIClient(self.user, self.session)
        balance_repo = AccountBalanceRepository(self.user, self.session)

        db_balance = balance_repo.get_by_account_id(account_id)

        if db_balance is not None and not db_balance.older_than(hours=6):
            # Local balance is updated
            balance = db_balance
        else:
            api_balance = gc_api.get_account_balances(account_id).available_amount

            if api_balance is None:
                # return seconds left until balance is available (check error message)
                raise FinanceServiceException(500, "Balance not found")

            if db_balance is None:
                balance = AccountBalance(
                    user_id=self.user.id,
                    account_id=account_id,
                    amount=Decimal(api_balance),
                )
                balance_repo.add(balance)
            else:
                db_balance.amount = Decimal(api_balance)
                balance = db_balance

        res = BankBalanceResponse(
            bank=institution_id, account_id=account_id, balance=float(balance.amount)
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
            bank_account_repo.add(
                BankAccount(
                    user_id=self.user.id,
                    id=account_id,
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
                    balance = self.fetch_gocardless_balance(
                        account.institution_id, account.id
                    )
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

    def get_bank_transactions(self) -> list[BankTransactionResponse]:
        """
        Fetches the latest transactions from the bank accounts.
        """
        gc_api = GoCardlessAPIClient(self.user, self.session)
        bank_account_repo = BankAccountRepository(self.user, self.session)
        bank_transaction_repo = BankTransactionRepository(self.user, self.session)

        transactions = []

        for account in bank_account_repo.get_all():
            # If the last sync was less than 6 hours ago, get the transactions from the database
            if account.last_synced > dt.datetime.now() - dt.timedelta(hours=6):
                for synced_transaction in bank_transaction_repo.get_by_account_id(
                    account.id
                ):
                    transactions.append(
                        BankTransactionResponse(
                            id=synced_transaction.id,
                            account_id=synced_transaction.account.id,
                            amount=float(synced_transaction.amount),
                            date=synced_transaction.date,
                            description=synced_transaction.description,
                            counterparty=synced_transaction.counterparty,
                        )
                    )
                continue

            account_transactions = gc_api.get_account_transactions(account.id).booked

            for transaction in account_transactions:
                if transaction.transactionId is None:
                    continue

                db_transaction = bank_transaction_repo.get_by_id(
                    account.id, transaction.transactionId
                )

                if db_transaction is None:
                    description = ""
                    if transaction.remittanceInformationUnstructured is not None:
                        description = transaction.remittanceInformationUnstructured
                    elif transaction.remittanceInformationUnstructuredArray is not None:
                        description = " ".join(
                            transaction.remittanceInformationUnstructuredArray
                        )

                    if transaction.valueDateTime is not None:
                        date = dt.datetime.fromisoformat(transaction.valueDateTime)
                    elif transaction.valueDate is not None:
                        date = dt.datetime.strptime(
                            transaction.valueDate, "%Y-%m-%d"
                        ).replace(hour=0, minute=0, second=0)
                    else:
                        date = dt.datetime.max

                    counterparty = (
                        transaction.debtorName
                        if transaction.debtorName
                        else transaction.creditorName
                    )

                    bank_transaction_repo.add(
                        BankTransaction(
                            user_id=self.user.id,
                            id=transaction.transactionId,
                            account_id=account.id,
                            amount=Decimal(transaction.transactionAmount.amount),
                            date=date,
                            description=description,
                            counterparty=counterparty,
                        )
                    )

                    transactions.append(
                        BankTransactionResponse(
                            id=transaction.transactionId,
                            account_id=account.id,
                            amount=float(transaction.transactionAmount.amount),
                            date=date,
                            description=description,
                            counterparty=counterparty,
                        )
                    )

                else:
                    transactions.append(
                        BankTransactionResponse(
                            id=db_transaction.id,
                            account_id=account.id,
                            amount=float(db_transaction.amount),
                            date=db_transaction.date,
                            description=db_transaction.description,
                            counterparty=db_transaction.counterparty,
                        )
                    )

            account.last_synced = dt.datetime.now()

        self.session.commit()

        return transactions

    def update_bank_transaction(
        self,
        account_id: str,
        transaction_id: str,
        user_description: Optional[str],
        subcategory_id: Optional[str],
    ) -> BankTransactionResponse:
        """
        Updates a bank transaction with user description and subcategory.
        """
        bank_transaction_repo = BankTransactionRepository(self.user, self.session)
        transaction = bank_transaction_repo.get_by_id(account_id, transaction_id)
        if transaction is None:
            raise FinanceServiceException(404, "Transaction not found")
        transaction.user_description = user_description
        if subcategory_id is not None:
            transaction.subcategory_id = uuid.UUID(subcategory_id)
        self.session.commit()
        return BankTransactionResponse(
            id=transaction.id,
            account_id=transaction.account.id,
            amount=float(transaction.amount),
            date=transaction.date,
            description=transaction.description,
            counterparty=transaction.counterparty,
        )

    def get_budget_categories(self) -> list[BudgetCategoryResponse]:
        """
        Fetches the budget categories and subcategories.
        """
        categories = []
        for category in self.user.budget_categories:
            subcategories = []
            for subcategory in category.subcategories:
                subcategories.append(
                    BudgetSubCategoryResponse(
                        id=str(subcategory.id),
                        name=subcategory.name,
                        category_id=str(category.id),
                        category_name=category.name,
                        budgeted=float(200),
                        spent=float(100),
                        available=float(100),
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

    def get_budget_category(self, category_id: str) -> BudgetCategoryResponse:
        """
        Fetches a budget category by ID.
        """
        category = self.session.query(BudgetCategory).get(category_id)
        if category is None:
            raise FinanceServiceException(404, "Category not found")
        subcategories = []
        for subcategory in category.subcategories:
            subcategories.append(
                BudgetSubCategoryResponse(
                    id=str(subcategory.id),
                    name=subcategory.name,
                    category_id=str(category.id),
                    category_name=category.name,
                    budgeted=float(200),
                    spent=float(100),
                    available=float(100),
                )
            )
        return BudgetCategoryResponse(
            id=str(category.id), name=category.name, subcategories=subcategories
        )

    def update_budget_category(
        self, category_id: str, name: str
    ) -> BudgetCategoryResponse:
        """
        Updates a budget category by ID.
        """
        category = self.session.query(BudgetCategory).get(category_id)
        if category is None:
            raise FinanceServiceException(404, "Category not found")
        category.name = name
        self.session.commit()
        return BudgetCategoryResponse(
            id=str(category.id), name=category.name, subcategories=[]
        )

    def delete_budget_category(self, category_id: str) -> None:
        """
        Deletes a budget category by ID.
        """
        category = self.session.query(BudgetCategory).get(category_id)
        if category is None:
            raise FinanceServiceException(404, "Category not found")
        self.session.delete(category)
        self.session.commit()

    def get_budget_subcategories(
        self, category_id: str
    ) -> list[BudgetSubCategoryResponse]:
        """
        Fetches the subcategories of a budget category.
        """
        category = self.session.query(BudgetCategory).get(category_id)
        if category is None:
            raise FinanceServiceException(404, "Category not found")
        subcategories = []
        for subcategory in category.subcategories:
            subcategories.append(
                BudgetSubCategoryResponse(
                    id=str(subcategory.id),
                    name=subcategory.name,
                    category_id=str(category.id),
                    category_name=category.name,
                    budgeted=float(200),
                    spent=float(100),
                    available=float(100),
                )
            )
        return subcategories

    def create_budget_subcategory(
        self, category_id: str, name: str, amount: float
    ) -> BudgetSubCategoryResponse:
        """
        Creates a new budget subcategory.
        """
        category = self.session.query(BudgetCategory).get(
            (uuid.UUID(category_id), self.user.id)
        )
        if category is None:
            raise FinanceServiceException(404, "Category not found")
        subcategory = BudgetSubCategory(
            user_id=self.user.id,
            category_id=category_id,
            name=name,
            amount=Decimal(amount),
        )
        category.subcategories.append(subcategory)
        self.session.commit()
        return BudgetSubCategoryResponse(
            id=str(subcategory.id),
            name=subcategory.name,
            category_id=str(category.id),
            category_name=category.name,
            budgeted=float(200),
            spent=float(100),
            available=float(100),
        )

    def update_budget_subcategory(
        self, subcategory_id: str, name: str, amount: float
    ) -> BudgetSubCategoryResponse:
        """
        Updates a budget subcategory by ID.
        """
        subcategory = self.session.query(BudgetSubCategory).get(subcategory_id)
        if subcategory is None:
            raise FinanceServiceException(404, "Subcategory not found")
        subcategory.name = name
        subcategory.amount = Decimal(amount)
        self.session.commit()
        return BudgetSubCategoryResponse(
            id=str(subcategory.id),
            name=subcategory.name,
            category_id=str(subcategory.category_id),
            category_name=subcategory.category.name,
            budgeted=float(200),
            spent=float(100),
            available=float(100),
        )

    def delete_budget_subcategory(self, subcategory_id: str) -> None:
        """
        Deletes a budget subcategory by ID.
        """
        subcategory = self.session.query(BudgetSubCategory).get(subcategory_id)
        if subcategory is None:
            raise FinanceServiceException(404, "Subcategory not found")
        self.session.delete(subcategory)
        self.session.commit()
