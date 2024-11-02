from fastapi import APIRouter, Depends

from lifehub.core.user.api.dependencies import user_is_authenticated

from .dependencies import RoutineServiceDep
from .models import TaskListResponse, TaskResponse

router = APIRouter(
    dependencies=[Depends(user_is_authenticated)],
)


@router.get("/tasks")
async def get_tasks(
    routine_service: RoutineServiceDep,
) -> list[TaskListResponse]:
    return routine_service.get_tasks()


@router.post("/tasks/{tasklist_id}/{task_id}/complete")
async def complete_task(
    routine_service: RoutineServiceDep,
    tasklist_id: str,
    task_id: str,
) -> TaskResponse:
    return routine_service.complete_task(tasklist_id, task_id)
