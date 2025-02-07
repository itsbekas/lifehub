import datetime as dt
import urllib.parse
from typing import Any

from sqlalchemy.orm import Session

from lifehub.core.common.base.api_client import APIClient, AuthType
from lifehub.core.user.schema import User

from .models import Calendar, CalendarEventsRequest, Event


class GoogleCalendarAPIClient(APIClient):
    provider_name = "google_calendar"
    base_url = "https://www.googleapis.com/calendar/v3"
    auth_type = AuthType.OAUTH

    def __init__(self, user: User, session: Session) -> None:
        super().__init__(user, session)

    def get_calendars(self) -> list[Calendar]:
        res = self._get("users/me/calendarList")
        data = res.get("items", [])
        return [Calendar.from_response(c) for c in data]

    def get_events(self, calendar_id: str, limit: int = 20) -> list[Event]:
        # url encode calendar_id
        calendar_id = urllib.parse.quote(calendar_id)
        params = CalendarEventsRequest(
            singleEvents=True,
            showDeleted=False,
            timeMin=dt.datetime.now().isoformat() + "Z",
            timeMax=(dt.datetime.now() + dt.timedelta(days=365)).isoformat() + "Z",
            maxResults=limit,
        )
        data = self._get(f"calendars/{calendar_id}/events", params=params).get(
            "items", []
        )
        return [Event.from_response(e) for e in data]

    def _test(self) -> None:
        self.get_calendars()

    def _error_msg(self, res: Any) -> str:
        msg: str = res.text
        return msg
