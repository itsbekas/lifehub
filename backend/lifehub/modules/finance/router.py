from typing import Any

from fastapi import APIRouter, Depends

from lifehub.core.common.api.dependencies import SessionDep
from lifehub.core.user.api.dependencies import UserDep, user_is_authenticated
from lifehub.providers.gocardless.api_client import GoCardlessAPIClient

from .dependencies import FinanceServiceDep
from .models import T212DataResponse

router = APIRouter(
    dependencies=[Depends(user_is_authenticated)],
)


@router.get("/trading212/data")
async def get_trading212_data(
    finance_service: FinanceServiceDep,
) -> T212DataResponse:
    return finance_service.get_t212_data()


@router.get("/test")
async def test(
    session: SessionDep,
    user: UserDep,
) -> Any:
    return GoCardlessAPIClient(user, session).create_agreement()
