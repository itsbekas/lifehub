from typing import Any

from sqlalchemy.orm import Session

from lifehub.config.constants import GOCARDLESS_BANK_ID, REDIRECT_URI_BASE
from lifehub.core.common.base.api_client import APIClient
from lifehub.core.user.schema import User

from .models import EndUserAgreementRequest, RequisitionRequest


class GoCardlessAPIClient(APIClient):
    provider_name = "gocardless"
    base_url = "https://bankaccountdata.gocardless.com/api/v2"

    def __init__(self, user: User, session: Session) -> None:
        super().__init__(user, session)
        self.headers = self._token_bearer_headers

    def _get(self, endpoint: str, params: dict[str, str] = {}) -> Any:
        return self._get_with_headers(endpoint, params=params)

    def _post(self, endpoint: str, data: dict[str, Any] = {}) -> Any:
        return self._post_with_headers(endpoint, data=data)

    def create_agreement(self) -> Any:
        req = EndUserAgreementRequest(
            institution_id=GOCARDLESS_BANK_ID,
        )
        res = self._post("agreements/enduser", data=req.dict())
        return res

    def create_requisition(self, req: RequisitionRequest) -> Any:
        req = RequisitionRequest(
            redirect=REDIRECT_URI_BASE,
            institution_id=GOCARDLESS_BANK_ID,
            agreement="agreement",
            reference="reference",
            user_language="en",
            ssn="123456789",
            account_selection=True,
            redirect_immediate=True,
        )
        res = self._post("requisitions", data=req.dict())
        return res

    def _test(self) -> None:
        pass

    def _error_msg(self, res: Any) -> str:
        msg: str = res.json().get("detail")
        return msg
