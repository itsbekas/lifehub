import uuid
from typing import Optional

from fastapi import APIRouter, Depends

from lifehub.core.common.base.pagination import PaginatedResponse
from lifehub.core.user.api.dependencies import user_is_authenticated

from .dependencies import BudgetServiceDep, FilterServiceDep, FinanceServiceDep
from .models import (
    BankBalanceResponse,
    BankInstitutionResponse,
    BankTransactionFilterRequest,
    BankTransactionFilterResponse,
    BankTransactionResponse,
    BudgetCategoryRequest,
    BudgetCategoryResponse,
    BudgetSubCategoryRequest,
    BudgetSubCategoryResponse,
    CountryResponse,
    UpdateBankTransactionRequest,
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


@router.post("/bank/add")
async def add_bank_account(
    finance_service: FinanceServiceDep,
    bank_id: str,
) -> None:
    return finance_service.add_bank_account(bank_id)


@router.post("/bank/callback")
async def confirm_bank_login(
    finance_service: FinanceServiceDep,
    ref: str,
) -> None:
    return finance_service.confirm_bank_login(ref)


@router.get("/bank/balances")
async def get_bank_balances(
    finance_service: FinanceServiceDep,
) -> list[BankBalanceResponse]:
    return finance_service.get_bank_balances()


@router.get("/bank/transactions")
async def get_bank_transactions(
    finance_service: FinanceServiceDep,
    page: int = 1,
    page_size: int = 20,
    subcategory_id: Optional[str] = None,
    description: Optional[str] = None,
) -> PaginatedResponse[BankTransactionResponse]:
    # Create a filter request from query parameters
    request = BankTransactionFilterRequest(
        page=page,
        page_size=page_size,
        subcategory_id=subcategory_id,
        description=description,
    )
    return finance_service.get_bank_transactions(request)


@router.get("/bank/transactions/filters")
async def get_bank_transactions_filters(
    filter_service: FilterServiceDep,
) -> list[BankTransactionFilterResponse]:
    return filter_service.get_bank_transactions_filters()


@router.post("/bank/transactions/filters")
async def create_bank_transactions_filter(
    filter_service: FilterServiceDep, data: BankTransactionFilterRequest
) -> BankTransactionFilterResponse:
    return filter_service.create_bank_transactions_filter(data)


@router.put("/bank/transactions/filters/{filter_id}")
async def update_bank_transactions_filter(
    filter_service: FilterServiceDep,
    filter_id: str,
    data: BankTransactionFilterRequest,
) -> BankTransactionFilterResponse:
    return filter_service.update_bank_transactions_filter(uuid.UUID(filter_id), data)


@router.put("/bank/{account_id}/transactions/{transaction_id}")
async def update_bank_transaction(
    finance_service: FinanceServiceDep,
    account_id: str,
    transaction_id: str,
    data: UpdateBankTransactionRequest,
) -> BankTransactionResponse:
    return finance_service.update_bank_transaction(
        uuid.UUID(account_id),
        uuid.UUID(transaction_id),
        data.description,
        data.subcategory_id,
        data.amount,
    )


@router.get("/bank/countries")
async def get_countries(
    finance_service: FinanceServiceDep,
) -> list[CountryResponse]:
    return finance_service.get_countries()


@router.get("/bank/banks")
async def get_banks(
    finance_service: FinanceServiceDep,
    country: str = "PT",  # Default to Portugal
) -> list[BankInstitutionResponse]:
    return finance_service.get_institutions(country)


@router.get("/budget/categories")
async def get_budget_categories(
    budget_service: BudgetServiceDep,
) -> list[BudgetCategoryResponse]:
    return budget_service.get_budget_categories()


@router.post("/budget/categories")
async def create_budget_category(
    budget_service: BudgetServiceDep,
    budget_category: BudgetCategoryRequest,
) -> BudgetCategoryResponse:
    return budget_service.create_budget_category(budget_category.name)


@router.get("/budget/categories/{category_id}")
async def get_budget_category(
    budget_service: BudgetServiceDep,
    category_id: str,
) -> BudgetCategoryResponse:
    return budget_service.get_budget_category(uuid.UUID(category_id))


@router.put("/budget/categories/{category_id}")
async def update_budget_category(
    budget_service: BudgetServiceDep,
    category_id: str,
    name: str,
) -> BudgetCategoryResponse:
    return budget_service.update_budget_category(uuid.UUID(category_id), name)


@router.delete("/budget/categories/{category_id}")
async def delete_budget_category(
    budget_service: BudgetServiceDep,
    category_id: str,
) -> None:
    budget_service.delete_budget_category(uuid.UUID(category_id))


@router.get("/budget/categories/{category_id}/subcategories")
async def get_budget_subcategories(
    budget_service: BudgetServiceDep,
    category_id: str,
) -> list[BudgetSubCategoryResponse]:
    return budget_service.get_budget_subcategories(uuid.UUID(category_id))


@router.post("/budget/categories/{category_id}/subcategories")
async def create_budget_subcategory(
    budget_service: BudgetServiceDep,
    category_id: str,
    data: BudgetSubCategoryRequest,
) -> BudgetSubCategoryResponse:
    return budget_service.create_budget_subcategory(
        uuid.UUID(category_id), data.name, data.amount
    )


@router.put("/budget/subcategories/{subcategory_id}")
async def update_budget_subcategory(
    budget_service: BudgetServiceDep,
    subcategory_id: str,
    data: BudgetSubCategoryRequest,
) -> BudgetSubCategoryResponse:
    return budget_service.update_budget_subcategory(
        uuid.UUID(subcategory_id), data.name, data.amount
    )


@router.delete("/budget/subcategories/{subcategory_id}")
async def delete_budget_subcategory(
    budget_service: BudgetServiceDep,
    subcategory_id: str,
) -> None:
    budget_service.delete_budget_subcategory(uuid.UUID(subcategory_id))
