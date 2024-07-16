from lifehub.providers.base.base_fetcher import BaseFetcher
from lifehub.providers.trading212.api_client import Trading212APIClient
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

        orders = t212.get_order_history()
        transactions = t212.get_transactions()
        balance = t212.get_account_cash()
        dividends = t212.get_dividends()

        order_db = T212OrderRepository(self.user, self.session)

        for order in orders:
            if order.date_modified > self.prev_timestamp:
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
            if transaction.date_time > self.prev_timestamp:
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
