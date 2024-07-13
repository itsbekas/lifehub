import datetime as dt

import pytz
from sqlalchemy.orm import Session

from lifehub.core.common.base_user_service import BaseUserService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.user.schema import User
from lifehub.providers.google_calendar.api_client import GoogleCalendarAPIClient
from lifehub.providers.google_calendar.models import Calendar, EventTime

from .models import CalendarResponse, EventResponse


class CalendarServiceException(ServiceException):
    def __init__(self, message: str):
        super().__init__("Calendar", message)


class CalendarService(BaseUserService):
    def __init__(self, session: Session, user: User):
        super().__init__(session, user)

    def get_calendars(self) -> list[CalendarResponse]:
        calendars: list[Calendar] = GoogleCalendarAPIClient(self.user).get_calendars()
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
        raise CalendarServiceException("Event start time not found")

    def get_events(self) -> list[EventResponse]:
        calendars = self.get_calendars()
        events = []
        for calendar in calendars:
            events.extend(
                [
                    EventResponse(
                        id=e.id,
                        summary=e.summary,
                        start=self._get_event_time_dt(e.start, calendar.timezone),
                        end=self._get_event_time_dt(e.end, calendar.timezone),
                        location=e.location,
                    )
                    for e in GoogleCalendarAPIClient(self.user).get_events(calendar.id)
                ]
            )
        return sorted(events, key=lambda e: e.start)
