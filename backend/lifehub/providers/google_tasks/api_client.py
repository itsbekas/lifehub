from typing import Any, Optional

from sqlalchemy.orm import Session

from lifehub.core.common.base.api_client import APIClient
from lifehub.core.user.schema import User

from .models import TaskListResponse, TaskResponse


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

    def get_tasklist(self, tasklist_id: str) -> TaskListResponse:
        res = self._get(f"users/@me/lists/{tasklist_id}")
        return TaskListResponse(**res)

    def list_tasklists(
        self, limit: int = 20, next_token: str = ""
    ) -> list[TaskListResponse]:
        params: dict[str, Any] = {"maxResults": limit}
        if next_token:
            params["pageToken"] = next_token
        task_lists = self._get("users/@me/lists", params=params).get("items", [])
        return [TaskListResponse(**item) for item in task_lists]

    def get_task(
        self,
        tasklist_id: str,
        task_id: str,
    ) -> TaskResponse:
        res = self._get(f"lists/{tasklist_id}/tasks/{task_id}")
        return TaskResponse(**res)

    def list_tasks(
        self,
        tasklist_id: str,
        completed_max: Optional[str] = None,
        completed_min: Optional[str] = None,
        due_max: Optional[str] = None,
        due_min: Optional[str] = None,
        max_results: int = 20,
        page_token: Optional[str] = None,
        show_completed: bool = True,
        show_deleted: bool = False,
        show_hidden: bool = False,
        updated_min: Optional[str] = None,
        show_assigned: bool = False,
    ) -> list[TaskResponse]:
        params: dict[str, Any] = {
            "maxResults": max_results,
            "showCompleted": show_completed,
            "showDeleted": show_deleted,
            "showHidden": show_hidden,
            "showAssigned": show_assigned,
        }
        if completed_max is not None:
            params["completedMax"] = completed_max
        if completed_min is not None:
            params["completedMin"] = completed_min
        if due_max is not None:
            params["dueMax"] = due_max
        if due_min is not None:
            params["dueMin"] = due_min
        if page_token is not None:
            params["pageToken"] = page_token
        if updated_min is not None:
            params["updatedMin"] = updated_min

        res = self._get(f"lists/{tasklist_id}/tasks", params=params).get("items", [])
        return [TaskResponse(**item) for item in res]

    def _test(self) -> None:
        self.list_tasklists(1)

    def _error_msg(self, res: Any) -> str:
        msg: str = res.text
        return msg
