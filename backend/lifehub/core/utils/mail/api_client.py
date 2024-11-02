from typing import Any

from lifehub.config.constants import POSTMARK_API_TOKEN, REDIRECT_URI_BASE
from lifehub.core.common.base.api_client import APIClient, AuthType
from lifehub.core.utils.mail.templates import verify_email


class MailAPIClient(APIClient):
    provider_name = "postmark"
    base_url = "https://api.postmarkapp.com"
    auth_type = AuthType.HEADERS

    def __init__(self) -> None:
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Postmark-Server-Token": POSTMARK_API_TOKEN,
        }

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
