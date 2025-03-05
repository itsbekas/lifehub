import uuid

from fastapi import APIRouter, Depends

from lifehub.core.user.api.dependencies import user_is_authenticated

from .dependencies import FinanceServiceDep
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


@router.post("/bank/callback")
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
) -> list[BankTransactionResponse]:
    return finance_service.get_bank_transactions()


@router.get("/bank/transactions/filters")
async def get_bank_transactions_filters(
    finance_service: FinanceServiceDep,
) -> list[BankTransactionFilterResponse]:
    return finance_service.get_bank_transactions_filters()


@router.post("/bank/transactions/filters")
async def create_bank_transactions_filter(
    finance_service: FinanceServiceDep, data: BankTransactionFilterRequest
) -> BankTransactionFilterResponse:
    return finance_service.create_bank_transactions_filter(data)


@router.put("/bank/transactions/filters/{filter_id}")
async def update_bank_transactions_filter(
    finance_service: FinanceServiceDep,
    filter_id: str,
    data: BankTransactionFilterRequest,
) -> BankTransactionFilterResponse:
    return finance_service.update_bank_transactions_filter(uuid.UUID(filter_id), data)


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


@router.get("/bank/banks")
async def get_banks(
    finance_service: FinanceServiceDep,
) -> list[BankInstitutionResponse]:
    return [
        BankInstitutionResponse(
            id="SANDBOXFINANCE_SFIN0000", name="Sandbox Finance", logo=""
        )
    ] + finance_service.get_institutions()


@router.get("/budget/categories")
async def get_budget_categories(
    finance_service: FinanceServiceDep,
) -> list[BudgetCategoryResponse]:
    return finance_service.get_budget_categories()


@router.post("/budget/categories")
async def create_budget_category(
    finance_service: FinanceServiceDep,
    budget_category: BudgetCategoryRequest,
) -> BudgetCategoryResponse:
    return finance_service.create_budget_category(budget_category.name)


@router.get("/budget/categories/{category_id}")
async def get_budget_category(
    finance_service: FinanceServiceDep,
    category_id: str,
) -> BudgetCategoryResponse:
    return finance_service.get_budget_category(uuid.UUID(category_id))


@router.put("/budget/categories/{category_id}")
async def update_budget_category(
    finance_service: FinanceServiceDep,
    category_id: str,
    name: str,
) -> BudgetCategoryResponse:
    return finance_service.update_budget_category(uuid.UUID(category_id), name)


@router.delete("/budget/categories/{category_id}")
async def delete_budget_category(
    finance_service: FinanceServiceDep,
    category_id: str,
) -> None:
    finance_service.delete_budget_category(uuid.UUID(category_id))


@router.get("/budget/categories/{category_id}/subcategories")
async def get_budget_subcategories(
    finance_service: FinanceServiceDep,
    category_id: str,
) -> list[BudgetSubCategoryResponse]:
    return finance_service.get_budget_subcategories(uuid.UUID(category_id))


@router.post("/budget/categories/{category_id}/subcategories")
async def create_budget_subcategory(
    finance_service: FinanceServiceDep,
    category_id: str,
    data: BudgetSubCategoryRequest,
) -> BudgetSubCategoryResponse:
    return finance_service.create_budget_subcategory(
        uuid.UUID(category_id), data.name, data.amount
    )


@router.put("/budget/subcategories/{subcategory_id}")
async def update_budget_subcategory(
    finance_service: FinanceServiceDep,
    subcategory_id: str,
    data: BudgetSubCategoryRequest,
) -> BudgetSubCategoryResponse:
    return finance_service.update_budget_subcategory(
        uuid.UUID(subcategory_id), data.name, data.amount
    )


@router.delete("/budget/subcategories/{subcategory_id}")
async def delete_budget_subcategory(
    finance_service: FinanceServiceDep,
    subcategory_id: str,
) -> None:
    finance_service.delete_budget_subcategory(uuid.UUID(subcategory_id))
