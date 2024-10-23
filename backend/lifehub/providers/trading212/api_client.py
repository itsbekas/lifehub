import datetime as dt
from typing import Any
from urllib.parse import parse_qs, urlparse

from sqlalchemy.orm import Session

from lifehub.core.common.api_client import APIClient, APIException
from lifehub.core.user.schema import User

from .models import AccountCash, AccountMetadata, Dividend, Order, Transaction


class Trading212APIClient(APIClient):
    provider_name = "trading212"
    base_url = "https://live.trading212.com/api/v0"

    def __init__(self, user: User, session: Session) -> None:
        super().__init__(user, session)
        self.headers = self._token_headers

    def _get(self, endpoint: str, params: dict[str, str] = {}) -> Any:
        # Handle 429: Too Many Requests
        return self._get_with_headers(endpoint, params=params)

    def _post(self, endpoint: str, data: dict[str, Any] = {}) -> Any:
        return self._post_with_headers(endpoint, data=data)

    def _test(self) -> None:
        self.get_account_metadata()

    def get_account_cash(self) -> AccountCash | None:
        res = self._get("equity/account/cash")
        return AccountCash.from_response(res)

    def get_account_metadata(self) -> AccountMetadata | None:
        res = self._get("equity/account/info")
        return AccountMetadata.from_response(res)

    def get_order_history(
        self, prev_timestamp: dt.datetime = dt.datetime(1970, 1, 1)
    ) -> list[Order]:
        orders = []
        stop = False
        params = {"limit": 50}
        # I'm pretty sure that the cursors returned by the API are wrong and useless
        # For reference, a cursor is the timestamp of the most recent order to be returned
        # The date used for the check is date_modified
        # If the cursor is before the date_created but after the date_modified, the order will be missed
        while not stop:
            res = self._get("equity/history/orders", params)
            order_data = res.get("items", [])
            for order in [Order.from_response(o) for o in order_data]:
                if order.date_modified < prev_timestamp:
                    stop = True
                    break
                orders.append(order)
            # Get the cursor for the next page
            params["cursor"] = int(order.date_created.timestamp() * 1000)
            if res.get("nextPagePath") is None:
                stop = True
        return orders

    def get_transactions(
        self, prev_timestamp: dt.datetime = dt.datetime(1970, 1, 1)
    ) -> list[Transaction]:
        transactions = []
        stop = False
        params = {"limit": 50}
        # Documentation for this endpoint is just plain wrong...
        # Instead of the cursor being a timestamp, the cursor is a reference to the last transaction
        # and needs to be used together with the time parameter
        # The cursor and time in nextPagePath both belong to the first transaction that wasn't returned
        while not stop:
            try:
                print("REQUEST:", params)
                res = self._get("history/transactions", params)
                print(res)
            # For some reason the API returns a 500 error whenever the limit is higher than the amount of transactions left
            # To fix this, we just halve the limit and try again until we get all transactions
            except APIException as e:
                if e.status_code == 500:
                    params["limit"] //= 2
                    if params["limit"] == 0:
                        stop = True
                    continue
                else:
                    raise e
            transaction_data = res.get("items", [])
            for transaction in [Transaction.from_response(t) for t in transaction_data]:
                if transaction.date_time < prev_timestamp:
                    stop = True
                    break
                transactions.append(transaction)
            nextPath = res.get("nextPagePath")
            if nextPath is None:
                stop = True
            else:
                # Get the cursor for the next page
                print(nextPath)
                query_params = parse_qs(urlparse(nextPath).query)
                print(query_params)
                params["cursor"] = query_params["cursor"][0]
                params["time"] = query_params["time"][0]
        return transactions

    def get_dividends(self) -> list[Dividend]:
        res = self._get("history/dividends")
        data = res.get("items", [])
        return [Dividend.from_response(d) for d in data]

    def _error_msg(self, res: Any) -> Any:
        return res.text
