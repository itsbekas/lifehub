from lifehub.providers.base.base_fetcher import BaseFetcher
from lifehub.providers.trading212.api_client import Trading212APIClient
from lifehub.providers.trading212.models import Order
from lifehub.providers.trading212.repository.t212_balance import T212BalanceRepository
from lifehub.providers.trading212.repository.t212_dividend import T212DividendRepository
from lifehub.providers.trading212.repository.t212_order import T212OrderRepository
from lifehub.providers.trading212.repository.t212_transaction import (
    T212TransactionRepository,
)
from lifehub.providers.trading212.schema import (
    T212Balance,
    T212Dividend,
    T212Order,
    T212Transaction,
)


class Trading212Fetcher(BaseFetcher):
    provider_name = "trading212"

    def fetch_data(self) -> None:
        t212 = Trading212APIClient(self.user, self.session)

        orders: list[Order] = t212.get_order_history(self.prev_timestamp)

        transactions = t212.get_transactions(self.prev_timestamp)
        balance = t212.get_account_cash()
        dividends = t212.get_dividends()
        balance = []
        dividends = []

        order_db = T212OrderRepository(self.user, self.session)

        for order in orders:
            quantity = order.filled_quantity

            if quantity is None:
                if order.fill_price is None or order.filled_value is None:
                    continue
                quantity = order.filled_value / order.fill_price

            new_order = T212Order(
                id=order.id,
                user_id=self.user.id,
                ticker=order.ticker,
                quantity=quantity,
                price=order.fill_price,
                timestamp=order.date_modified,
            )
            order_db.add(new_order)

        transaction_db = T212TransactionRepository(self.user, self.session)

        for transaction in transactions:
            new_transaction = T212Transaction(
                id=transaction.reference,
                user_id=self.user.id,
                amount=transaction.amount,
                timestamp=transaction.date_time,
            )
            transaction_db.add(new_transaction)

        balance_db = T212BalanceRepository(self.user, self.session)

        if balance:
            new_balance = T212Balance(
                user_id=self.user.id,
                free=balance.free,
                invested=balance.invested,
                result=balance.ppl,
            )
            balance_db.add(new_balance)

        dividend_db = T212DividendRepository(self.user, self.session)

        for dividend in dividends:
            if dividend.paid_on > self.prev_timestamp:
                new_dividend = T212Dividend(
                    id=dividend.reference,
                    user_id=self.user.id,
                    ticker=dividend.ticker,
                    amount=dividend.amount,
                    quantity=dividend.quantity,
                    timestamp=dividend.paid_on,
                )
                dividend_db.add(new_dividend)
