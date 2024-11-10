from sqlalchemy.orm import Session

from lifehub.core.common.base.service.user import BaseUserService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.user.schema import User
from lifehub.providers.gocardless.api_client import GoCardlessAPIClient
from lifehub.providers.trading212.repository.t212_balance import T212BalanceRepository
from lifehub.providers.trading212.repository.t212_dividend import T212DividendRepository
from lifehub.providers.trading212.repository.t212_order import T212OrderRepository
from lifehub.providers.trading212.repository.t212_transaction import (
    T212TransactionRepository,
)
from lifehub.providers.trading212.schema import T212Balance

from .models import (
    BankBalanceResponse,
    T212BalanceResponse,
    T212DataResponse,
    T212TransactionResponse,
)
from .repository import BankAccountRepository
from .schema import BankAccount


class FinanceServiceException(ServiceException):
    def __init__(self, status_code: int, message: str):
        super().__init__("Finance", status_code, message)


class FinanceService(BaseUserService):
    def __init__(self, session: Session, user: User):
        super().__init__(session, user)

    def get_t212_balance(self) -> T212BalanceResponse:
        balance: T212Balance | None = T212BalanceRepository(
            self.user, self.session
        ).get_latest()

        if balance is None:
            raise FinanceServiceException(404, "Balance not found")

        return T212BalanceResponse(
            timestamp=balance.timestamp,
            free=float(balance.free),
            invested=float(balance.invested),
            result=float(balance.result),
        )

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
        balance = self.get_t212_balance()
        history = self.get_t212_history()
        return T212DataResponse(balance=balance, history=history)

    def get_bank_login(self) -> str:
        api = GoCardlessAPIClient(self.user, self.session)
        return api.create_requisition().link

    def confirm_bank_login(self, ref: str) -> None:
        api = GoCardlessAPIClient(self.user, self.session)
        requisition = api.get_requisition(ref)
        bank_account_repo = BankAccountRepository(self.session)
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
        api = GoCardlessAPIClient(self.user, self.session)
        ba_repo = BankAccountRepository(self.session)
        balances = []
        for account in ba_repo.get_by_user_id(self.user.id):
            api_balances = api.get_account_balances(account.account_id)
            # get the balance that has balanceType == "interimAvailable"
            balance = next(
                (b for b in api_balances if b.balanceType == "interimAvailable"), None
            )
            if balance is not None:
                balances.append(
                    BankBalanceResponse(
                        bank=account.institution_id,
                        balance=float(balance.balanceAmount.amount),
                    )
                )
        return balances
