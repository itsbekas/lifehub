from typing import Any

import requests as rq
from sqlalchemy.orm import Session

from lifehub.core.common.api_client import APIClient
from lifehub.core.user.schema import User

from .models import MainData


class QBittorrentAPIClient(APIClient):
    provider_name = "qbittorrent"
    base_url = "https://qb.b21.tech/api/v2"

    def __init__(self, user: User, session: Session) -> None:
        super().__init__(user, session)
        username, password = self.token.token.split(":")
        headers = {"Referer": "https://qb.b21.tech/"}
        auth_data = {"username": username, "password": password}
        res = rq.post(f"{self.base_url}/auth/login", headers=headers, data=auth_data)
        self.cookies: dict[str, str] = res.cookies.get_dict()

    def _get(self, endpoint: str, params: dict[str, str] = {}) -> Any:
        return self._get_with_cookies(endpoint, params)

    def _post(self, endpoint: str, data: dict[str, str] = {}) -> Any:
        return self._post_with_cookies(endpoint, data)

    def get_main_data(self) -> MainData | None:
        res = self._get("sync/maindata")
        return MainData.from_response(res)

    def _test(self) -> None:
        self.get_main_data()

    def _error_msg(self, res: rq.Response) -> str:
        return res.text
