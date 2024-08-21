from typing import Any

from sqlalchemy.orm import Session

from lifehub.core.common.api_client import APIClient
from lifehub.core.user.schema import User

from .models import User as SpotifyUser


class SpotifyAPIClient(APIClient):
    provider_name = "spotify"
    base_url = "https://api.spotify.com/v1"

    def __init__(self, session: Session, user: User) -> None:
        super().__init__(session, user)
        self.headers = self._token_bearer_headers

    def _get(self, endpoint: str, params: dict[str, str] = {}) -> Any:
        return self._get_with_headers(endpoint, params=params)

    def _post(self, endpoint: str, data: dict[str, Any] = {}) -> Any:
        return self._post_with_headers(endpoint, data=data)

    def _test(self) -> None:
        self.get_current_user()

    def get_current_user(self) -> SpotifyUser | None:
        res = self._get("me")
        return SpotifyUser.from_response(res)

    def _error_msg(self, res: Any) -> str:
        return res.json().get("error", {}).get("message", "Unknown error")
