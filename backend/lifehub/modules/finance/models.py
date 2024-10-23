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
