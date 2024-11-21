from typing import Any

from fastapi import APIRouter, Depends

from lifehub.core.user.api.dependencies import user_is_authenticated

from .dependencies import FinanceServiceDep
from .models import BankBalanceResponse, T212DataResponse

router = APIRouter(
    dependencies=[Depends(user_is_authenticated)],
)


@router.get("/trading212/data")
async def get_trading212_data(
    finance_service: FinanceServiceDep,
) -> T212DataResponse:
    return finance_service.get_t212_data()


@router.get("/bank/login")
async def get_bank_login(
    finance_service: FinanceServiceDep,
    bank_id: str,
) -> str:
    return finance_service.get_bank_login(bank_id)


@router.get("/bank/confirm-login")
async def confirm_bank_login(finance_service: FinanceServiceDep, ref: str) -> None:
    return finance_service.confirm_bank_login(ref)


@router.get("/bank/balances")
async def get_bank_balances(
    finance_service: FinanceServiceDep,
) -> list[BankBalanceResponse]:
    return finance_service.get_bank_balances()


@router.get("/bank/transactions")
async def get_bank_transactions(
    finance_service: FinanceServiceDep,
) -> list[Any]:
    return finance_service.get_bank_transactions()


@router.get("/bank/banks")
async def get_banks(
    finance_service: FinanceServiceDep,
) -> list[Any]:
    return []
