from fastapi import APIRouter, Depends

from lifehub.core.user.api.dependencies import user_is_authenticated

from .dependencies import CalendarServiceDep
from .models import CalendarResponse, EventResponse

router = APIRouter(
    dependencies=[Depends(user_is_authenticated)],
)


@router.get("/calendars")
async def get_calendars(
    calendar_service: CalendarServiceDep,
) -> list[CalendarResponse]:
    return calendar_service.get_calendars()


@router.get("/events")
async def get_events(
    calendar_service: CalendarServiceDep,
    limit: int = 20,
) -> list[EventResponse]:
    return calendar_service.get_events(limit)
