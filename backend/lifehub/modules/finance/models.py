from __future__ import annotations

import datetime as dt
from typing import Optional

from pydantic.dataclasses import dataclass


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
class BankInstitutionResponse:
    id: str
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
class BankTransactionFilterRequest:
    subcategory_id: Optional[str]
    description: Optional[str]
    matches: list[str]


@dataclass
class BankTransactionFilterResponse:
    id: str
    matches: list[str]
    subcategory_id: Optional[str]
    description: Optional[str]
