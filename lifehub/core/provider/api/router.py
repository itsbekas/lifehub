from fastapi import APIRouter, Depends, HTTPException

from lifehub.core.provider.api.dependencies import (
    ProviderDep,
    ProviderServiceDep,
)
from lifehub.core.provider.models import ProviderWithModulesResponse
from lifehub.core.provider.schema import is_oauth_config
from lifehub.core.user.api.dependencies import user_is_authenticated

router = APIRouter(
    dependencies=[Depends(user_is_authenticated)],
)


@router.get("")
async def get_providers(
    provider_service: ProviderServiceDep,
) -> list[ProviderWithModulesResponse]:
    return provider_service.get_providers_with_modules()


@router.get("/{provider_id}/oauth_url")
async def oauth_authorization_url(provider: ProviderDep) -> str:
    if not is_oauth_config(provider.config):
        raise HTTPException(404, "Provider must be an OAuth provider")
    auth_url: str = provider.config.build_auth_url()
    if provider.name == "google_calendar":
        auth_url += "&access_type=offline&prompt=consent"
    return auth_url
