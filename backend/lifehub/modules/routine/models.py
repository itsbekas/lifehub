import datetime as dt
from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class TaskResponse:
    id: str
    title: str
    due: Optional[str]
    completed: Optional[str]


@dataclass
class TaskListResponse:
    id: str
    title: str
    tasks: list[TaskResponse]


@dataclass
class CalendarResponse:
    id: str
    summary: str
    timezone: str


@dataclass
class EventResponse:
    id: str
    title: str
    start: dt.datetime
    end: dt.datetime
    location: str
