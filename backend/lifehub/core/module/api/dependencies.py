from typing import Annotated

from fastapi import Depends

from lifehub.core.common.api.dependencies import SessionDep
from lifehub.core.module.schema import Module
from lifehub.core.module.service.module import ModuleService


def get_module_service(session: SessionDep) -> ModuleService:
    return ModuleService(session)


ModuleServiceDep = Annotated[ModuleService, Depends(get_module_service)]


def get_module(
    module_id: int,
    module_service: ModuleServiceDep,
) -> Module:
    return module_service.get_module_by_id(module_id)


ModuleDep = Annotated[Module, Depends(get_module)]
