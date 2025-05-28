from fastapi import APIRouter, Depends

from lifehub.core.provider.api.dependencies import ProviderDep, ProviderServiceDep
from lifehub.core.provider.models import ProviderResponse
from lifehub.core.user.api.dependencies import user_is_authenticated

router = APIRouter(
    dependencies=[Depends(user_is_authenticated)],
)


@router.get("")
async def get_providers(
    provider_service: ProviderServiceDep,
) -> list[ProviderResponse]:
    return provider_service.get_providers()


@router.get("/{provider_id}/oauth_url")
async def oauth_authorization_url(
    provider: ProviderDep,
    provider_service: ProviderServiceDep,
) -> str:
    oauth_config = provider_service.get_oauth_config(
        provider
    )  # Use getter for type safety
    auth_url: str = oauth_config.build_auth_url()
    if provider.name == "google_calendar":
        auth_url += "&access_type=offline&prompt=consent"
    return auth_url
