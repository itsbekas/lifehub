import datetime as dt
from decimal import Decimal
from typing import Any

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
    BankTransactionResponse,
    T212DataResponse,
    T212TransactionResponse,
)
from .repository import (
    AccountBalanceRepository,
    BankAccountRepository,
    BankTransactionRepository,
)
from .schema import AccountBalance, BankAccount, BankTransaction


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

        res = BankBalanceResponse(bank="trading212", balance=float(balance.amount))
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

        res = BankBalanceResponse(bank=institution_id, balance=float(balance.amount))
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

    def get_t212_data(self) -> T212DataResponse:
        balance = self.fetch_t212_balance()
        history = self.get_t212_history()
        return T212DataResponse(balance=balance, history=history)

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
                    account_id=account_id,
                    institution_id=requisition.institution_id,
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
            balances.append(
                self.fetch_gocardless_balance(
                    account.institution_id, account.account_id
                )
            )

        balances.append(self.fetch_t212_balance())

        return balances

    def get_bank_transactions(self) -> list[Any]:
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
                    account.account_id
                ):
                    transactions.append(
                        BankTransactionResponse(
                            transaction_id=synced_transaction.transaction_id,
                            account_id=synced_transaction.account_id,
                            amount=float(synced_transaction.amount),
                            date=synced_transaction.date,
                            description=synced_transaction.description,
                            counterparty=synced_transaction.counterparty,
                        )
                    )
                continue

            account_transactions = gc_api.get_account_transactions(
                account.account_id
            ).booked

            for transaction in account_transactions:
                if transaction.transactionId is None:
                    continue

                db_transaction = bank_transaction_repo.get_by_id(
                    account.account_id, transaction.transactionId
                )

                if db_transaction is None:
                    description = ""
                    if transaction.remittanceInformationUnstructured is not None:
                        description = transaction.remittanceInformationUnstructured
                    elif transaction.remittanceInformationUnstructuredArray is not None:
                        description = " ".join(
                            transaction.remittanceInformationUnstructuredArray
                        )

                    date = (
                        transaction.valueDateTime
                        if transaction.valueDateTime
                        else transaction.valueDate
                    )

                    counterparty = (
                        transaction.debtorName
                        if transaction.debtorName
                        else transaction.creditorName
                    )

                    bank_transaction_repo.add(
                        BankTransaction(
                            user_id=self.user.id,
                            transaction_id=transaction.transactionId,
                            account_id=account.account_id,
                            amount=Decimal(transaction.transactionAmount.amount),
                            date=date,
                            description=description,
                            counterparty=counterparty,
                        )
                    )

                    transactions.append(
                        BankTransactionResponse(
                            transaction_id=transaction.transactionId,
                            account_id=account.account_id,
                            amount=float(transaction.transactionAmount.amount),
                            date=date,
                            description=description,
                            counterparty=counterparty,
                        )
                    )

                else:
                    transactions.append(
                        BankTransactionResponse(
                            transaction_id=db_transaction.transaction_id,
                            account_id=db_transaction.account_id,
                            amount=float(db_transaction.amount),
                            date=db_transaction.date,
                            description=db_transaction.description,
                            counterparty=db_transaction.counterparty,
                        )
                    )

        self.session.commit()

        return transactions
