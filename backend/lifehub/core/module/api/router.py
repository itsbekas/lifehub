from fastapi import APIRouter, Depends

from lifehub.core.module.api.dependencies import ModuleServiceDep
from lifehub.core.module.models import ModuleWithProvidersResponse
from lifehub.core.user.api.dependencies import user_is_authenticated

router = APIRouter(
    dependencies=[Depends(user_is_authenticated)],
)


@router.get("")
async def get_modules(
    module_service: ModuleServiceDep,
) -> list[ModuleWithProvidersResponse]:
    return module_service.get_modules_with_providers()
