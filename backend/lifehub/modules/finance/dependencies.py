from typing import Annotated

from fastapi import Depends

from lifehub.core.common.api.dependencies import SessionDep
from lifehub.core.user.api.dependencies import UserDep
from lifehub.modules.finance.service.budget_service import BudgetService
from lifehub.modules.finance.service.filter_service import FilterService
from lifehub.modules.finance.service.finance_service import FinanceService


def get_finance_service(session: SessionDep, user: UserDep) -> FinanceService:
    return FinanceService(session, user)


def get_budget_service(session: SessionDep, user: UserDep) -> BudgetService:
    return BudgetService(session, user)


def get_filter_service(session: SessionDep, user: UserDep) -> FilterService:
    return FilterService(session, user)


FinanceServiceDep = Annotated[FinanceService, Depends(get_finance_service)]

BudgetServiceDep = Annotated[BudgetService, Depends(get_budget_service)]

FilterServiceDep = Annotated[FilterService, Depends(get_filter_service)]
