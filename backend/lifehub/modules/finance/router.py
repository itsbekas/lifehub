from typing import Any

from fastapi import APIRouter, Depends

from lifehub.core.user.api.dependencies import user_is_authenticated

from .dependencies import FinanceServiceDep
from .models import (
    BankBalanceResponse,
    BankInstitutionResponse,
    BudgetCategoryResponse,
    BudgetSubCategoryResponse,
)

router = APIRouter(
    dependencies=[Depends(user_is_authenticated)],
)


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
) -> list[BankInstitutionResponse]:
    return finance_service.get_institutions()


@router.get("/budget/categories")
async def get_budget_categories(
    finance_service: FinanceServiceDep,
) -> list[BudgetCategoryResponse]:
    return finance_service.get_budget_categories()


@router.post("/budget/categories")
async def create_budget_category(
    finance_service: FinanceServiceDep,
    name: str,
) -> BudgetCategoryResponse:
    return finance_service.create_budget_category(name)


@router.get("/budget/categories/{category_id}")
async def get_budget_category(
    finance_service: FinanceServiceDep,
    category_id: str,
) -> BudgetCategoryResponse:
    return finance_service.get_budget_category(category_id)


@router.put("/budget/categories/{category_id}")
async def update_budget_category(
    finance_service: FinanceServiceDep,
    category_id: str,
    name: str,
) -> BudgetCategoryResponse:
    return finance_service.update_budget_category(category_id, name)


@router.delete("/budget/categories/{category_id}")
async def delete_budget_category(
    finance_service: FinanceServiceDep,
    category_id: str,
) -> None:
    finance_service.delete_budget_category(category_id)


@router.get("/budget/categories/{category_id}/subcategories")
async def get_budget_subcategories(
    finance_service: FinanceServiceDep,
    category_id: str,
) -> list[BudgetSubCategoryResponse]:
    return finance_service.get_budget_subcategories(category_id)


@router.post("/budget/categories/{category_id}/subcategories")
async def create_budget_subcategory(
    finance_service: FinanceServiceDep,
    category_id: str,
    name: str,
    amount: float,
) -> BudgetSubCategoryResponse:
    return finance_service.create_budget_subcategory(category_id, name, amount)


@router.put("/budget/subcategories/{subcategory_id}")
async def update_budget_subcategory(
    finance_service: FinanceServiceDep,
    subcategory_id: str,
    name: str,
    amount: float,
) -> BudgetSubCategoryResponse:
    return finance_service.update_budget_subcategory(subcategory_id, name, amount)


@router.delete("/budget/subcategories/{subcategory_id}")
async def delete_budget_subcategory(
    finance_service: FinanceServiceDep,
    subcategory_id: str,
) -> None:
    finance_service.delete_budget_subcategory(subcategory_id)
