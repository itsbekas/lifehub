import datetime as dt
import urllib.parse
from typing import Any

from lifehub.core.common.api_client import APIClient
from lifehub.core.user.schema import User

from .models import Calendar, Event


class GoogleCalendarAPIClient(APIClient):
    provider_name = "google_calendar"
    base_url = "https://www.googleapis.com/calendar/v3"

    def __init__(self, user: User) -> None:
        super().__init__(user)
        self.headers = self._token_bearer_headers

    def _get(self, endpoint: str, params: dict[str, str] = {}) -> Any:
        return self._get_with_headers(endpoint, params=params)

    def _post(self, endpoint: str, data: dict[str, Any] = {}) -> Any:
        return self._post_with_headers(endpoint, data=data)

    def get_calendars(self) -> list[Calendar]:
        res = self._get("users/me/calendarList")
        data = res.get("items", [])
        return [Calendar.from_response(c) for c in data]

    def get_events(self, calendar_id: str) -> list[Event]:
        # url encode calendar_id
        calendar_id = urllib.parse.quote(calendar_id)
        res = self._get(
            f"calendars/{calendar_id}/events",
            {
                "singleEvents": "true",
                "showDeleted": "false",
                "timeMin": dt.datetime.now().isoformat() + "Z",
                "timeMax": (dt.datetime.now() + dt.timedelta(days=365)).isoformat()
                + "Z",
            },
        )
        data = res.get("items", [])
        return [Event.from_response(e) for e in data]

    def _test(self) -> None:
        self.get_calendars()

    def _error_msg(self, res: Any) -> Any:
        return res.text
