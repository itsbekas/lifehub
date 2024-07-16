from typing import Any

from sqlalchemy.orm import Session

from lifehub.core.common.api_client import APIClient
from lifehub.core.user.schema import User

from .models import AccountCash, AccountMetadata, Dividend, Order, Transaction


class Trading212APIClient(APIClient):
    provider_name = "trading212"
    base_url = "https://live.trading212.com/api/v0"

    def __init__(self, user: User, session: Session) -> None:
        super().__init__(user, session)
        self.headers = self._token_headers

    def _get(self, endpoint: str, params: dict[str, str] = {}) -> Any:
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

    def get_order_history(self) -> list[Order]:
        res = self._get("equity/history/orders")
        data = res.get("items", [])
        return [Order.from_response(o) for o in data]

    def get_transactions(self) -> list[Transaction]:
        res = self._get("history/transactions")
        data = res.get("items", [])
        return [Transaction.from_response(t) for t in data]

    def get_dividends(self) -> list[Dividend]:
        res = self._get("history/dividends")
        data = res.get("items", [])
        return [Dividend.from_response(d) for d in data]

    def _error_msg(self, res: Any) -> Any:
        return res.text
