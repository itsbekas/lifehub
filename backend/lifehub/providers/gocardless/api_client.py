import datetime as dt
from typing import Any

from sqlalchemy.orm import Session

from lifehub.config.constants import (
    ADMIN_USERNAME,
    GOCARDLESS_BANK_ID,
    GOCARDLESS_CLIENT_ID,
    GOCARDLESS_CLIENT_SECRET,
    REDIRECT_URI_BASE,
)
from lifehub.core.common.base.api_client import APIClient
from lifehub.core.provider.repository.provider_token import ProviderTokenRepository
from lifehub.core.user.schema import User

from .models import (
    EndUserAgreementRequest,
    JWTObtainPairRequest,
    JWTRefreshRequest,
    RequisitionRequest,
    SpectacularJWTObtainResponse,
    SpectacularJWTRefreshResponse,
)


class GoCardlessAPIClient(APIClient):
    provider_name = "gocardless"
    base_url = "https://bankaccountdata.gocardless.com/api/v2"

    def __init__(self, user: User, session: Session) -> None:
        super().__init__(user, session, ADMIN_USERNAME)
        self.headers = self._token_bearer_headers

    def _refresh_token(self, tokenRepo: ProviderTokenRepository) -> None:
        res = self.refresh_token()
        self.token.token = res.access
        self.token.expires_at = dt.datetime.now() + dt.timedelta(seconds=res.access_expires)
        tokenRepo.update(self.token)

    def _get(self, endpoint: str, params: Any = {}) -> Any:
        return self._get_with_headers(endpoint, params=params)

    def _post(self, endpoint: str, data: Any = {}) -> Any:
        return self._post_with_headers(endpoint, data=data)

    def get_token(self) -> SpectacularJWTObtainResponse:
        req = JWTObtainPairRequest(
            secret_id=GOCARDLESS_CLIENT_ID,
            secret_key=GOCARDLESS_CLIENT_SECRET,
        )
        res = self._post_basic("token/new/", data=req)
        return SpectacularJWTObtainResponse(**res)

    def refresh_token(self) -> SpectacularJWTRefreshResponse:
        req = JWTRefreshRequest(refresh=self.token.refresh_token)
        res = self._post_basic("token/refresh/", data=req)
        return SpectacularJWTRefreshResponse(**res)

    def create_agreement(self) -> Any:
        req = EndUserAgreementRequest(
            institution_id=GOCARDLESS_BANK_ID,
        )
        res = self._post("agreements/enduser/", data=req)
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
        res = self._post("requisitions", data=req)
        return res

    def get_institution(self, institution_id: str) -> Any:
        return self._get(f"institutions/{institution_id}/")

    def _test(self) -> None:
        self.get_institution(GOCARDLESS_BANK_ID)

    def _error_msg(self, res: Any) -> str:
        msg: str = res.json().get("detail")
        return msg
