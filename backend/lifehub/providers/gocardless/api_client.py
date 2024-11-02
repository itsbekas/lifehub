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
from lifehub.core.common.base.api_client import APIClient, AuthType, auth_override
from lifehub.core.provider.repository.provider_token import ProviderTokenRepository
from lifehub.core.user.schema import User

from .models import (
    EndUserAcceptanceDetailsRequest,
    EndUserAgreementRequest,
    EndUserAgreementResponse,
    JWTObtainPairRequest,
    JWTRefreshRequest,
    RequisitionRequest,
    RequisitionsRequest,
    SpectacularJWTObtainResponse,
    SpectacularJWTRefreshResponse,
    SpectacularRequisitionResponse,
)


class GoCardlessAPIClient(APIClient):
    provider_name = "gocardless"
    base_url = "https://bankaccountdata.gocardless.com/api/v2"
    auth_type = AuthType.OAUTH

    def __init__(self, user: User, session: Session) -> None:
        super().__init__(user, session, ADMIN_USERNAME)

    def _refresh_token(self, tokenRepo: ProviderTokenRepository) -> None:
        res = self.refresh_token()
        self.token.token = res.access
        self.token.expires_at = dt.datetime.now() + dt.timedelta(
            seconds=res.access_expires
        )
        tokenRepo.update(self.token)

    @auth_override(AuthType.BASIC)
    def get_token(self) -> SpectacularJWTObtainResponse:
        req = JWTObtainPairRequest(
            secret_id=GOCARDLESS_CLIENT_ID,
            secret_key=GOCARDLESS_CLIENT_SECRET,
        )
        res = self._post("token/new/", data=req)
        return SpectacularJWTObtainResponse(**res)

    def refresh_token(self) -> SpectacularJWTRefreshResponse:
        req = JWTRefreshRequest(refresh=self.token.refresh_token)
        res = self._post("token/refresh/", data=req)
        return SpectacularJWTRefreshResponse(**res)

    def create_agreement(self) -> EndUserAgreementResponse:
        req = EndUserAgreementRequest(
            institution_id=GOCARDLESS_BANK_ID,
        )
        res = self._post("agreements/enduser/", data=req)
        return EndUserAgreementResponse(**res)

    def accept_agreement(
        self, agreement_id: str, user_agent: str, ip_address: str
    ) -> EndUserAgreementResponse:
        req = EndUserAcceptanceDetailsRequest(
            user_agent=user_agent,
            ip_address=ip_address,
        )
        res = self._put(f"agreements/enduser/{agreement_id}/accept/", data=req)
        return EndUserAgreementResponse(**res)

    def get_requisitions(self, limit: int = 100, offset: int = 0) -> Any:
        params = RequisitionsRequest(
            limit=limit,
            offset=offset,
        )
        return self._get("requisitions", params=params)

    def create_requisition(self, agreement_id: str, user_id: str) -> Any:
        req = RequisitionRequest(
            redirect=REDIRECT_URI_BASE,
            institution_id=GOCARDLESS_BANK_ID,
            agreement=agreement_id,
            reference=user_id,
            user_language="en",
            ssn=None,
            account_selection=False,
            redirect_immediate=False,
        )
        res = self._post("requisitions", data=req)
        return SpectacularRequisitionResponse(**res)

    def get_institution(self, institution_id: str) -> Any:
        return self._get(f"institutions/{institution_id}/")

    def _test(self) -> None:
        self.get_institution(GOCARDLESS_BANK_ID)

    def _error_msg(self, res: Any) -> str:
        msg: str = res.json().get("detail")
        return msg
