from fastapi import APIRouter, Depends

from lifehub.core.user.api.dependencies import user_is_authenticated

from .dependencies import RoutineServiceDep
from .models import TaskListResponse

router = APIRouter(
    dependencies=[Depends(user_is_authenticated)],
)


@router.get("/tasks")
async def get_tasks(
    routine_service: RoutineServiceDep,
) -> list[TaskListResponse]:
    return routine_service.get_tasks()
