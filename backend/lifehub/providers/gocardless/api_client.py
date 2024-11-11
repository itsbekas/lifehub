import datetime as dt
from typing import Any, Optional

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
    AccountBalance,
    AccountBalances,
    EndUserAcceptanceDetailsRequest,
    EndUserAgreementRequest,
    EndUserAgreementResponse,
    InstitutionResponse,
    InstitutionsRequest,
    JWTObtainPairRequest,
    JWTRefreshRequest,
    RequisitionRequest,
    RequisitionsRequest,
    SpectacularJWTObtainResponse,
    SpectacularJWTRefreshResponse,
    SpectacularRequisitionResponse,
    TransactionsRequest,
    TransactionsResponse,
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

    def get_account_metadata(self, account_id: str) -> Any:
        return self._get(f"accounts/{account_id}/")

    def get_account_balances(self, account_id: str) -> AccountBalances:
        res = self._get(f"accounts/{account_id}/balances/")
        if res is None:
            return AccountBalances(balances=[])
        return AccountBalances(
            balances=[AccountBalance(**balance) for balance in res.get("balances")]
        )

    def get_account_details(self, account_id: str) -> Any:
        return self._get(f"accounts/{account_id}/details/")

    def get_account_transactions(
        self,
        account_id: str,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> TransactionsResponse:
        req = TransactionsRequest(
            date_from=date_from,
            date_to=date_to,
        )
        res = self._get(f"accounts/{account_id}/transactions/", params=req).get(
            "transactions"
        )
        return TransactionsResponse(**res)

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

    def get_institutions(self, country: str = "PT") -> list[InstitutionResponse]:
        req = InstitutionsRequest(country=country)
        res = self._get("institutions", params=req)
        return [InstitutionResponse(**inst) for inst in res]

    def get_institution(self, institution_id: str) -> InstitutionResponse:
        res = self._get(f"institutions/{institution_id}/")
        return InstitutionResponse(**res)

    def get_requisitions(self, limit: int = 100, offset: int = 0) -> Any:
        params = RequisitionsRequest(
            limit=limit,
            offset=offset,
        )
        return self._get("requisitions", params=params)

    def create_requisition(self, bank_id: str) -> SpectacularRequisitionResponse:
        req = RequisitionRequest(redirect=REDIRECT_URI_BASE, institution_id=bank_id)
        res = self._post("requisitions", data=req).get("results")[0]
        return SpectacularRequisitionResponse(**res)

    def get_requisition(self, requisition_id: str) -> SpectacularRequisitionResponse:
        res = self._get(f"requisitions/{requisition_id}/")
        return SpectacularRequisitionResponse(**res)

    def _test(self) -> None:
        self.get_institution(GOCARDLESS_BANK_ID)

    def _error_msg(self, res: Any) -> str:
        msg: str = res.json().get("detail")
        return msg
