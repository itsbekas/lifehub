import datetime as dt

from pydantic.dataclasses import dataclass


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
