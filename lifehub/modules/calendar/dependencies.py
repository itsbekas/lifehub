from typing import Annotated

from fastapi import Depends

from lifehub.core.common.api.dependencies import SessionDep
from lifehub.core.user.api.dependencies import UserDep
from lifehub.modules.calendar.service import CalendarService


def get_calendar_service(session: SessionDep, user: UserDep) -> CalendarService:
    return CalendarService(session, user)


CalendarServiceDep = Annotated[CalendarService, Depends(get_calendar_service)]
