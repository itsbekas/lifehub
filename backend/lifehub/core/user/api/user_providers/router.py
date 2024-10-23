import base64 as b64
import datetime as dt

import requests
from fastapi import APIRouter, Depends, HTTPException

from lifehub.config.constants import OAUTH_REDIRECT_URI
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


@router.get("/missing")
async def get_missing_providers(
    user: UserDep, user_service: UserServiceDep
) -> list[ProviderWithModulesResponse]:
    return user_service.get_missing_providers_with_modules(user)


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
    # TODO: Move this code to a service
    url = provider.config.build_token_url(code)
    data = {}
    params = {}
    headers = {}

    if provider.id == "spotify":
        url = provider.config.token_url
        headers = {
            "Authorization": "Basic "
            + b64.b64encode(
                f"{provider.config.client_id}:{provider.config.client_secret}".encode(
                    "utf-8"
                )
            ).decode("utf-8"),
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": OAUTH_REDIRECT_URI,
        }

    res = requests.post(url, data=data, params=params, headers=headers)
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
    user_service.add_provider_token_to_user(
        user, provider, req.token, None, None, None, req.custom_url
    )


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
        user,
        provider,
        f"{req.username}:{req.password}",
        None,
        None,
        None,
        req.custom_url,
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


@router.post("/{provider_id}/test")
async def test_user_provider_connection(
    provider: ProviderDep, user: UserDep, user_service: UserServiceDep
) -> None:
    user_service.test_provider_token(user, provider)
