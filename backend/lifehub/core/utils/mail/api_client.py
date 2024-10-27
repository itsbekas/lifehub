from typing import Any

from lifehub.config.constants import POSTMARK_API_TOKEN, REDIRECT_URI_BASE
from lifehub.core.common.base.api_client import APIClient
from lifehub.core.utils.mail.templates import verify_email


class MailAPIClient(APIClient):
    provider_name = "postmark"
    base_url = "https://api.postmarkapp.com"

    def __init__(self) -> None:
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Postmark-Server-Token": POSTMARK_API_TOKEN,
        }

    def _get(self, endpoint: str, params: dict[str, Any] = {}) -> Any:
        return self._get_with_headers(endpoint, params=params)

    def _post(self, endpoint: str, data: dict[str, Any] = {}) -> Any:
        # return self._post_with_headers(endpoint, data)
        # Mail API isn't working, so we'll just skip this for now
        pass

    def _put(self, endpoint: str, data: dict[str, Any] = {}) -> Any:
        return self._put_with_headers(endpoint, data=data)

    def send_verification_email(
        self, email: str, name: str, verification_token: str
    ) -> None:
        verification_link = (
            f"{REDIRECT_URI_BASE}/auth/verify-email?token={verification_token}"
        )

        data = {
            "From": "lifehub@b21.tech",
            "To": email,
            "Subject": "[Lifehub] Verify your email address",
            "HtmlBody": verify_email(name, verification_link),
            "MessageStream": "outbound",
        }
        self._post("email", data=data)

    def _test(self) -> None:
        raise NotImplementedError

    def _error_msg(self, res: Any) -> Any:
        return res.json()
