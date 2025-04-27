from __future__ import annotations

import datetime as dt
from dataclasses import field
from typing import Optional

from pydantic.dataclasses import dataclass

from lifehub.core.common.base.pagination import PaginatedRequest


@dataclass
class T212BalanceResponse:
    timestamp: dt.datetime
    free: float
    invested: float
    result: float


@dataclass
class T212TransactionResponse:
    timestamp: dt.datetime
    amount: float
    type: str
    ticker: Optional[str]


@dataclass
class T212DataResponse:
    balance: T212BalanceResponse
    history: list[T212TransactionResponse]


@dataclass
class BankBalanceResponse:
    bank: str
    account_id: str
    balance: float


@dataclass
class BankTransactionResponse:
    id: str
    account_id: str
    amount: float
    date: Optional[dt.datetime]
    description: Optional[str]
    counterparty: Optional[str]
    subcategory_id: Optional[str]


@dataclass
class CountryResponse:
    code: str
    name: str


@dataclass
class BankInstitutionResponse:
    id: str
    type: str
    name: str
    logo: str


@dataclass
class BudgetSubCategoryResponse:
    id: str
    name: str
    category_id: str
    category_name: str
    budgeted: float
    spent: float
    available: float


@dataclass
class BudgetCategoryRequest:
    name: str


@dataclass
class BudgetCategoryResponse:
    id: str
    name: str
    subcategories: list[BudgetSubCategoryResponse]


@dataclass
class BudgetSubCategoryRequest:
    name: str
    amount: float


@dataclass
class UpdateBankTransactionRequest:
    description: Optional[str]
    subcategory_id: Optional[str]
    amount: Optional[float]


@dataclass
class BankTransactionFilterRequest(PaginatedRequest):
    """Request model for filtering bank transactions with pagination."""

    subcategory_id: Optional[str] = None
    description: Optional[str] = None
    matches: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass
class BankTransactionFilterResponse:
    id: str
    matches: list[str]
    subcategory_id: Optional[str]
    description: Optional[str]
