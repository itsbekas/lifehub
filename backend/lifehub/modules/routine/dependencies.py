from typing import Annotated

from fastapi import Depends

from lifehub.core.common.api.dependencies import SessionDep
from lifehub.core.user.api.dependencies import UserDep
from lifehub.modules.routine.service import RoutineService


def get_routine_service(session: SessionDep, user: UserDep) -> RoutineService:
    return RoutineService(session, user)


RoutineServiceDep = Annotated[RoutineService, Depends(get_routine_service)]
