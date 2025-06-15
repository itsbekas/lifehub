from __future__ import annotations

import datetime as dt
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


@dataclass
class T212ExportTransaction:
    action: str
    time: str
    isin: Optional[str]
    ticker: Optional[str]
    name: Optional[str]
    notes: Optional[str]
    id: Optional[str]
    no_shares: Optional[float]
    share_price: Optional[float]
    currency: Optional[str]
    exchange_rate: Optional[float]
    result: Optional[float]
    result_currency: Optional[str]
    total: float
    total_currency: str
    withholding_tax: Optional[float]
    withholding_tax_currency: Optional[str]
    merchant_name: Optional[str]
    merchant_category: Optional[str]

    @staticmethod
    def from_csv(row: list[str]) -> T212ExportTransaction:
        return T212ExportTransaction(
            action=row[0],
            time=row[1],
            isin=row[2],
            ticker=row[3],
            name=row[4],
            notes=row[5],
            id=row[6],
            no_shares=float(row[7]) if row[7] else None,
            share_price=float(row[8]) if row[8] else None,
            currency=row[9],
            exchange_rate=float(row[10])
            if row[10] and row[10] != "Not available"
            else None,
            result=float(row[11]) if row[11] else None,
            result_currency=row[12],
            total=float(row[13]),
            total_currency=row[14],
            withholding_tax=float(row[15]) if row[15] else None,
            withholding_tax_currency=row[16],
            merchant_name=row[17],
            merchant_category=row[18],
        )
