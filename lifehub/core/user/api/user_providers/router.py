import datetime as dt

import requests
from fastapi import APIRouter, Depends, HTTPException

from lifehub.core.provider.api.dependencies import (
    ProviderDep,
)
from lifehub.core.provider.models import (
    ProviderTokenBasicRequest,
    ProviderTokenTokenRequest,
    ProviderWithModulesResponse,
)
from lifehub.core.provider.schema import (
    is_basic_config,
    is_oauth_config,
    is_token_config,
)
from lifehub.core.user.api.dependencies import (
    UserDep,
    UserServiceDep,
    user_is_authenticated,
)
from lifehub.core.user.api.user_providers.exceptions import (
    OAuthTokenRequestFailedException,
)

router = APIRouter(
    dependencies=[Depends(user_is_authenticated)],
)


@router.get("")
async def get_user_providers(
    user: UserDep, user_service: UserServiceDep
) -> list[ProviderWithModulesResponse]:
    return user_service.get_user_providers_with_modules(user)


@router.delete("/{provider_id}")
async def remove_user_provider(
    user: UserDep,
    provider: ProviderDep,
    user_service: UserServiceDep,
) -> None:
    user_service.remove_provider_from_user(user, provider)


@router.post("/{provider_id}/oauth_token")
async def add_oauth_provider(
    provider: ProviderDep,
    user: UserDep,
    user_service: UserServiceDep,
    code: str,
) -> None:
    if not is_oauth_config(provider.config):
        raise HTTPException(404, "Provider must be an OAuth provider")
    url = provider.config.build_token_url(code)
    res = requests.post(url)
    if res.status_code != 200:
        raise OAuthTokenRequestFailedException(res)
    data = res.json()

    if "created_at" in data:
        created_at = dt.datetime.fromtimestamp(data["created_at"])
    else:
        created_at = dt.datetime.now()
    expires_at: dt.datetime = created_at + dt.timedelta(seconds=data["expires_in"])

    user_service.add_provider_token_to_user(
        user,
        provider,
        data["access_token"],
        data["refresh_token"],
        created_at,
        expires_at,
    )


@router.post("/{provider_id}/basic_token")
async def add_token_provider(
    provider: ProviderDep,
    user: UserDep,
    user_service: UserServiceDep,
    req: ProviderTokenTokenRequest,
) -> None:
    if not is_token_config(provider.config):
        raise HTTPException(404, "Provider must be a token provider")
    user_service.add_provider_token_to_user(user, provider, req.token, None, None, None)


@router.patch("/{provider_id}/basic_token")
async def update_basic_token(
    provider: ProviderDep,
    user: UserDep,
    user_service: UserServiceDep,
    req: ProviderTokenTokenRequest,
) -> None:
    if not is_token_config(provider.config):
        raise HTTPException(404, "Provider must be a token provider")
    user_service.update_provider_token(user, provider, req.token)


@router.post("/{provider_id}/basic_login")
async def add_basic_provider(
    provider: ProviderDep,
    user: UserDep,
    user_service: UserServiceDep,
    req: ProviderTokenBasicRequest,
) -> None:
    if not is_basic_config(provider.config):
        raise HTTPException(404, "Provider must be a basic login provider")
    user_service.add_provider_token_to_user(
        user, provider, f"{req.username}:{req.password}", None, None, None
    )


@router.patch("/{provider_id}/basic_login")
async def update_basic_login(
    provider: ProviderDep,
    user: UserDep,
    user_service: UserServiceDep,
    req: ProviderTokenBasicRequest,
) -> None:
    if not is_basic_config(provider.config):
        raise HTTPException(404, "Provider must be a basic login provider")
    user_service.update_provider_token(user, provider, f"{req.username}:{req.password}")


# @router.get("/{provider_id}/test")
# async def test_user_provider_connection(provider: ProviderDep, user: UserDep):
#     APIClient = api_clients.get(provider.name)
#     try:
#         client = APIClient(user)
#     except AttributeError:
#         raise NoTokenException()

#     if not client.test_connection():
#         raise InvalidTokenException()
