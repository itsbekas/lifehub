from fastapi import APIRouter, Depends

from lifehub.core.module.api.dependencies import ModuleDep
from lifehub.core.module.models import ModuleWithProvidersResponse
from lifehub.core.user.api.dependencies import (
    UserDep,
    UserServiceDep,
    user_is_authenticated,
)

router = APIRouter(
    dependencies=[Depends(user_is_authenticated)],
)


@router.get("")
async def get_user_modules(
    user: UserDep, user_service: UserServiceDep
) -> list[ModuleWithProvidersResponse]:
    return user_service.get_user_modules_with_providers(user)


@router.post("/{module_id}")
async def add_user_module(
    user: UserDep,
    module: ModuleDep,
    user_service: UserServiceDep,
) -> None:
    user_service.add_module_to_user(user, module)


@router.delete("/{module_id}")
async def remove_user_module(
    user: UserDep,
    module: ModuleDep,
    user_service: UserServiceDep,
) -> None:
    user_service.remove_module_from_user(user, module)
