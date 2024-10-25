from typing import Any

from sqlalchemy.orm import Session

from lifehub.core.common.base.api_client import APIClient
from lifehub.core.user.schema import User

from .models import DetailedAthlete


class StravaAPIClient(APIClient):
    provider_name = "strava"
    base_url = "https://www.strava.com/api/v3"

    def __init__(self, session: Session, user: User) -> None:
        super().__init__(session, user)
        self.headers = self._token_bearer_headers

    def _get(self, endpoint: str, params: dict[str, str] = {}) -> Any:
        return self._get_with_headers(endpoint, params=params)

    def _post(self, endpoint: str, data: dict[str, Any] = {}) -> Any:
        return self._post_with_headers(endpoint, data=data)

    def _test(self) -> None:
        self.get_athlete()

    def get_athlete(self) -> DetailedAthlete | None:
        res = self._get("athlete")
        return DetailedAthlete.from_response(res)

    def _error_msg(self, res: Any) -> str:
        return res.json().get("message", "Unknown error")
