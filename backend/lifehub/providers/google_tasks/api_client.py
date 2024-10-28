from typing import Any

from sqlalchemy.orm import Session

from lifehub.core.common.base.api_client import APIClient
from lifehub.core.user.schema import User

from .models import TaskListResponse


class GoogleTasksAPIClient(APIClient):
    provider_name = "google_tasks"
    base_url = "https://www.googleapis.com/tasks/v1"

    def __init__(self, user: User, session: Session) -> None:
        super().__init__(user, session)
        self.headers = self._token_bearer_headers

    def _get(self, endpoint: str, params: dict[str, str] = {}) -> Any:
        return self._get_with_headers(endpoint, params=params)

    def _post(self, endpoint: str, data: dict[str, Any] = {}) -> Any:
        return self._post_with_headers(endpoint, data=data)

    def _put(self, endpoint: str, data: dict[str, Any] = {}) -> Any:
        return self._put_with_headers(endpoint, data=data)

    def list_tasklists(
        self, limit: int = 20, next_token: str = ""
    ) -> list[TaskListResponse]:
        params: dict[str, Any] = {"maxResults": limit}
        if next_token:
            params["pageToken"] = next_token
        task_lists = self._get("users/@me/lists", params=params).get("items", [])
        return [TaskListResponse(**item) for item in task_lists]

    def _test(self) -> None:
        self.list_tasklists(1)

    def _error_msg(self, res: Any) -> str:
        msg: str = res.text
        return msg
