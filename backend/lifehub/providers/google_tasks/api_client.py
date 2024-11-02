from typing import Any, Optional

from sqlalchemy.orm import Session

from lifehub.core.common.base.api_client import APIClient, AuthType
from lifehub.core.user.schema import User

from .models import (
    ListTasklistsRequest,
    ListTasksRequest,
    TaskListResponse,
    TaskResponse,
    TaskUpdateRequest,
)


class GoogleTasksAPIClient(APIClient):
    provider_name = "google_tasks"
    base_url = "https://www.googleapis.com/tasks/v1"
    auth_type = AuthType.OAUTH

    def __init__(self, user: User, session: Session) -> None:
        super().__init__(user, session)

    def get_tasklist(self, tasklist_id: str) -> TaskListResponse:
        res = self._get(f"users/@me/lists/{tasklist_id}")
        return TaskListResponse(**res)

    def list_tasklists(
        self, limit: int = 20, next_token: Optional[str] = None
    ) -> list[TaskListResponse]:
        params = ListTasklistsRequest(maxResults=limit, pageToken=next_token)
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
        params = ListTasksRequest(
            completedMax=completed_max,
            completedMin=completed_min,
            dueMax=due_max,
            dueMin=due_min,
            maxResults=max_results,
            pageToken=page_token,
            showCompleted=show_completed,
            showDeleted=show_deleted,
            showHidden=show_hidden,
            updatedMin=updated_min,
            showAssigned=show_assigned,
        )

        res = self._get(f"lists/{tasklist_id}/tasks", params).get("items", [])
        return [TaskResponse(**item) for item in res]

    def update_task(
        self,
        tasklist_id: str,
        task_id: str,
        task: TaskUpdateRequest,
    ) -> TaskResponse:
        res = self._patch(
            f"lists/{tasklist_id}/tasks/{task_id}",
            json=task,
        )
        return TaskResponse(**res)

    def _test(self) -> None:
        self.list_tasklists(1)

    def _error_msg(self, res: Any) -> str:
        return str(res.json().get("error", {}).get("message", res.text))
