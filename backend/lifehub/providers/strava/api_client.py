from typing import Any

from sqlalchemy.orm import Session

from lifehub.core.common.base.api_client import APIClient, AuthType
from lifehub.core.user.schema import User

from .models import DetailedAthlete


class StravaAPIClient(APIClient):
    provider_name = "strava"
    base_url = "https://www.strava.com/api/v3"
    auth_type = AuthType.OAUTH

    def __init__(self, user: User, session: Session) -> None:
        super().__init__(user, session)

    def _test(self) -> None:
        self.get_athlete()

    def get_athlete(self) -> DetailedAthlete | None:
        res = self._get("athlete")
        return DetailedAthlete.from_response(res)

    def _error_msg(self, res: Any) -> str:
        msg: str = res.json().get("message", "Unknown error")
        return msg
