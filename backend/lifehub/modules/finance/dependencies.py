from typing import Annotated

from fastapi import Depends

from lifehub.core.common.api.dependencies import SessionDep
from lifehub.core.user.api.dependencies import UserDep
from lifehub.modules.finance.service import FinanceService


def get_finance_service(session: SessionDep, user: UserDep) -> FinanceService:
    return FinanceService(session, user)


FinanceServiceDep = Annotated[FinanceService, Depends(get_finance_service)]
