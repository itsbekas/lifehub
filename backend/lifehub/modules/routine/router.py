from fastapi import APIRouter, Depends

from lifehub.core.user.api.dependencies import user_is_authenticated

from .dependencies import RoutineServiceDep
from .models import CalendarResponse, EventResponse, TaskListResponse, TaskResponse

router = APIRouter(
    dependencies=[Depends(user_is_authenticated)],
)


@router.get("/tasks")
async def get_tasks(
    routine_service: RoutineServiceDep, show_completed: bool = False
) -> list[TaskListResponse]:
    return routine_service.get_tasks(show_completed)


@router.patch("/tasks/{tasklist_id}/{task_id}/toggle")
async def toggle_task(
    routine_service: RoutineServiceDep, tasklist_id: str, task_id: str
) -> TaskResponse:
    return routine_service.toggle_task(tasklist_id, task_id)


@router.get("/events/calendars")
async def get_calendars(
    routine_service: RoutineServiceDep,
) -> list[CalendarResponse]:
    return routine_service.get_calendars()


@router.get("/events")
async def get_events(
    routine_service: RoutineServiceDep,
    limit: int = 20,
) -> list[EventResponse]:
    return routine_service.get_events(limit)
