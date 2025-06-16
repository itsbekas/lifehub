from __future__ import annotations

import datetime as dt
from typing import Optional

from pydantic import BaseModel, Field
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
class CreateBudgetCategoryRequest:
    name: str


@dataclass
class UpdateBudgetCategoryRequest:
    name: str


@dataclass
class BudgetCategoryResponse:
    id: str
    name: str
    subcategories: list[BudgetSubCategoryResponse]


@dataclass
class CreateBudgetSubCategoryRequest:
    name: str
    amount: float


@dataclass
class UpdateBudgetSubCategoryRequest:
    name: str
    amount: float


@dataclass
class UpdateBankTransactionRequest:
    description: Optional[str]
    subcategory_id: Optional[str]
    amount: Optional[float]


class GetBankTransactionsRequest(PaginatedRequest):
    subcategory_id: Optional[str] = None
    description: Optional[str] = None


@dataclass
class CreateBankTransactionFilterRequest:
    description: Optional[str]
    subcategory_id: Optional[str]


@dataclass
class BankTransactionFilterResponse:
    id: str
    matches: list[str]
    subcategory_id: Optional[str]
    description: Optional[str]


class T212ExportTransaction(BaseModel):
    action: str = Field(
        ...,
        alias="Action",
    )
    time: str = Field(
        ...,
        alias="Time",
    )  # e.g., "2023-10-01 12:34:56.789" or "2023-10-01 12:34:56"
    isin: Optional[str] = Field(
        None,
        alias="ISIN",
    )
    ticker: Optional[str] = Field(
        None,
        alias="Ticker",
    )
    name: Optional[str] = Field(
        None,
        alias="Name",
    )
    notes: Optional[str] = Field(
        None,
        alias="Notes",
    )
    id: Optional[str] = Field(
        None,
        alias="ID",
    )
    no_shares: Optional[float] = Field(
        None,
        alias="No. of shares",
    )
    share_price: Optional[float] = Field(
        None,
        alias="Price / share",
    )
    currency: Optional[str] = Field(
        None,
        alias="Currency (Price / share)",
    )
    exchange_rate: Optional[float] = Field(
        None,
        alias="Exchange rate",
    )
    result: Optional[float] = Field(
        None,
        alias="Result",
    )
    result_currency: Optional[str] = Field(None, alias="Currency (Result)")
    total: float = Field(
        ...,
        alias="Total",
    )
    total_currency: str = Field(
        ...,
        alias="Currency (Total)",
    )
    withholding_tax: Optional[float] = Field(
        None,
        alias="Withholding tax",
    )
    withholding_tax_currency: Optional[str] = Field(
        None,
        alias="Currency (Withholding tax)",
    )
    merchant_name: Optional[str] = Field(
        None,
        alias="Merchant name",
    )
    merchant_category: Optional[str] = Field(
        None,
        alias="Merchant category",
    )
