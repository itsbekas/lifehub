from fastapi import APIRouter, Depends

from lifehub.core.user.api.dependencies import user_is_authenticated

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
