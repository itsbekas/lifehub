import datetime as dt

import pytz
from sqlalchemy.orm import Session

import lifehub.providers.google_tasks.models as gt_models
from lifehub.core.common.base.service.user import BaseUserService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.user.schema import User
from lifehub.providers.google_calendar.api_client import GoogleCalendarAPIClient
from lifehub.providers.google_calendar.models import Calendar, EventTime
from lifehub.providers.google_tasks.api_client import GoogleTasksAPIClient

from .models import CalendarResponse, EventResponse, TaskListResponse, TaskResponse


class RoutineServiceException(ServiceException):
    def __init__(self, status_code: int, message: str):
        super().__init__("Routine", status_code, message)


class RoutineService(BaseUserService):
    def __init__(self, session: Session, user: User):
        super().__init__(session, user)

    def get_calendars(self) -> list[CalendarResponse]:
        calendars: list[Calendar] = GoogleCalendarAPIClient(
            self.user, self.session
        ).get_calendars()
        return [
            CalendarResponse(
                id=c.id,
                summary=c.summary,
                timezone=c.timeZone,
            )
            for c in calendars
        ]

    def _get_event_time_dt(self, event_time: EventTime, timezone: str) -> dt.datetime:
        if event_time.date_time:
            return event_time.date_time
        if event_time.date:
            tz = pytz.timezone(timezone)
            tz_date: dt.datetime = tz.localize(event_time.date)
            return tz_date
        raise RoutineServiceException(400, "Event start time not found")

    def get_events(self, limit: int = 20) -> list[EventResponse]:
        calendars = self.get_calendars()
        events = []
        for calendar in calendars:
            events.extend(
                [
                    EventResponse(
                        id=e.id,
                        title=e.summary,
                        start=self._get_event_time_dt(e.start, calendar.timezone),
                        end=self._get_event_time_dt(e.end, calendar.timezone),
                        location=e.location,
                    )
                    for e in GoogleCalendarAPIClient(
                        self.user, self.session
                    ).get_events(calendar.id, limit)
                ]
            )
        return sorted(events, key=lambda e: e.start)[:limit]

    def get_task(self, tasklist_id: str, task_id: str) -> TaskResponse:
        api_client = GoogleTasksAPIClient(self.user, self.session)
        task = api_client.get_task(tasklist_id, task_id)
        return TaskResponse(id=task.id, title=task.title, due=task.due, completed=task.completed)

    def get_tasks(self, show_completed: bool = False) -> list[TaskListResponse]:
        api_client = GoogleTasksAPIClient(self.user, self.session)

        tasklists = []

        for tasklist in api_client.list_tasklists():
            tasklists.append(
                TaskListResponse(id=tasklist.id, title=tasklist.title, tasks=[])
            )

            for task in api_client.list_tasks(tasklist.id, show_completed=show_completed):
                tasklists[-1].tasks.append(
                    TaskResponse(
                        id=task.id,
                        title=task.title,
                        due=task.due,
                        completed=task.completed,
                    )
                )

        return tasklists

    def toggle_task(
        self, tasklist_id: str, task_id: str
    ) -> TaskResponse:
        api_client = GoogleTasksAPIClient(self.user, self.session)
        task = api_client.get_task(tasklist_id, task_id)
        updated_task = api_client.update_task(
            tasklist_id,
            task_id,
            gt_models.TaskCompleteRequest(
                status="completed" if task.completed is None else "needsAction"
            ),
        )
        if updated_task.completed is None:
            raise RoutineServiceException(500, "Failed to complete task")
        return self.get_task(tasklist_id, task_id)
