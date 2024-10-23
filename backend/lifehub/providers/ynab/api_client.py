import re
from typing import Any

from sqlalchemy.orm import Session

from lifehub.core.common.api_client import APIClient
from lifehub.core.user.schema import User

from .models import Account, CategoryGroup


class YNABAPIClient(APIClient):
    provider_name = "ynab"
    base_url = "https://api.ynab.com/v1"

    budget = "last-used"

    def __init__(self, user: User, session: Session) -> None:
        super().__init__(user, session)
        self.headers = self._token_bearer_headers

    def _get(self, endpoint: str, params: dict[str, str] = {}) -> Any:
        return self._get_with_headers(endpoint, params=params)

    def _post(self, endpoint: str, data: dict[str, Any] = {}) -> Any:
        return self._post_with_headers(endpoint, data=data)

    def _test(self) -> None:
        self.get_user()

    def get_user(self) -> Any:
        return self._get("user")

    def get_budgets(self) -> Any:
        return self._get("budgets")

    def get_budget(self, budget: str = "last-used") -> Any:
        return self._get(f"budgets/{budget}")

    def get_budget_settings(self, budget: str = "last-used") -> Any:
        return self._get(f"budgets/{budget}/settings")

    def get_accounts(self, budget: str = "last-used") -> list[Account]:
        res = self._get(f"budgets/{budget}/accounts")
        data = res.get("data", {}).get("accounts", [])
        return [Account.from_response(a) for a in data]

    def get_account(self, account: str) -> Any:
        return self._get(f"budgets/{self.budget}/accounts/{account}")

    def get_categories(self) -> list[CategoryGroup]:
        res = self._get(f"budgets/{self.budget}/categories")
        data = res.get("data", {}).get("category_groups", [])
        return [CategoryGroup.from_response(c) for c in data]

    def get_category(self, category: str) -> Any:
        return self._get(f"budgets/{self.budget}/categories/{category}")

    def get_category_month(self, category: str, month: str) -> Any:
        if not re.match(r"\d{4}-\d{2}", month):
            raise Exception(
                "Can't retrieve category month. Month must be in format YYYY-MM-DD"
            )
        return self._get(f"budgets/{self.budget}/months/{month}/categories/{category}")

    def _error_msg(self, res: Any) -> Any:
        return res.json().get("error", {}).get("detail")
