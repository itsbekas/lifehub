from sqlalchemy.orm import Session

from lifehub.core.common.base.service.user import BaseUserService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.user.schema import User
from lifehub.modules.finance.models import (
    T212BalanceResponse,
    T212DataResponse,
    T212TransactionResponse,
)
from lifehub.providers.trading212.repository.t212_balance import T212BalanceRepository
from lifehub.providers.trading212.repository.t212_dividend import T212DividendRepository
from lifehub.providers.trading212.repository.t212_order import T212OrderRepository
from lifehub.providers.trading212.repository.t212_transaction import (
    T212TransactionRepository,
)
from lifehub.providers.trading212.schema import T212Balance


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
