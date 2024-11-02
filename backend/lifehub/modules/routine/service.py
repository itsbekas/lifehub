from sqlalchemy.orm import Session

from lifehub.core.common.base.service.user import BaseUserService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.user.schema import User
from lifehub.providers.google_tasks.api_client import GoogleTasksAPIClient

from .models import TaskListResponse, TaskResponse


class RoutineServiceException(ServiceException):
    def __init__(self, status_code: int, message: str):
        super().__init__("Routine", status_code, message)


class RoutineService(BaseUserService):
    def __init__(self, session: Session, user: User):
        super().__init__(session, user)

    def get_tasks(self) -> list[TaskListResponse]:
        api_client = GoogleTasksAPIClient(self.user, self.session)

        tasklists = []

        for tasklist in api_client.list_tasklists():
            tasklists.append(
                TaskListResponse(id=tasklist.id, title=tasklist.title, tasks=[])
            )

            for task in api_client.list_tasks(tasklist.id, show_completed=False):
                tasklists[-1].tasks.append(
                    TaskResponse(id=task.id, title=task.title, due=task.due)
                )

        return tasklists
