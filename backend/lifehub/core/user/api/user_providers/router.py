from fastapi import APIRouter, Depends

from lifehub.core.provider.api.dependencies import ProviderDep, ProviderServiceDep
from lifehub.core.provider.models import (
    ProviderWithModulesResponse,
    UpdateProviderTokenBasicRequest,
    UpdateProviderTokenTokenRequest,
)
from lifehub.core.user.api.dependencies import (
    UserDep,
    UserServiceDep,
    user_is_authenticated,
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
    provider_service: ProviderServiceDep,
    code: str,
) -> None:
    provider_service.validate_oauth_provider(provider)
    access_token, refresh_token, created_at, expires_at = (
        provider_service.process_oauth_token(provider, code)
    )
    user_service.add_provider_token_to_user(
        user,
        provider,
        access_token,
        refresh_token,
        created_at,
        expires_at,
    )


@router.post("/{provider_id}/basic_token")
async def add_token_provider(
    provider: ProviderDep,
    user: UserDep,
    user_service: UserServiceDep,
    provider_service: ProviderServiceDep,
    req: UpdateProviderTokenTokenRequest,
) -> None:
    provider_service.validate_token_provider(provider)
    user_service.add_provider_token_to_user(
        user, provider, req.token, None, None, None, req.custom_url
    )


@router.patch("/{provider_id}/basic_token")
async def update_basic_token(
    provider: ProviderDep,
    user: UserDep,
    user_service: UserServiceDep,
    provider_service: ProviderServiceDep,
    req: UpdateProviderTokenTokenRequest,
) -> None:
    provider_service.validate_token_provider(provider)
    user_service.update_provider_token(user, provider, req.token)


@router.post("/{provider_id}/basic_login")
async def add_basic_provider(
    provider: ProviderDep,
    user: UserDep,
    user_service: UserServiceDep,
    provider_service: ProviderServiceDep,
    req: UpdateProviderTokenBasicRequest,
) -> None:
    provider_service.validate_basic_provider(provider)
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
    provider_service: ProviderServiceDep,
    req: UpdateProviderTokenBasicRequest,
) -> None:
    provider_service.validate_basic_provider(provider)
    user_service.update_provider_token(user, provider, f"{req.username}:{req.password}")


@router.post("/{provider_id}/test")
async def test_user_provider_connection(
    provider: ProviderDep, user: UserDep, user_service: UserServiceDep
) -> None:
    user_service.test_provider_token(user, provider)
