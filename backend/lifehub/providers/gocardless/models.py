from __future__ import annotations

from dataclasses import asdict, field
from typing import Any, List, Literal

from pydantic.dataclasses import dataclass


@dataclass
class RequisitionRequest:
    redirect: str
    institution_id: str
    agreement: str
    reference: str
    user_language: str
    ssn: str
    account_selection: bool
    redirect_immediate: bool

    def dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class EndUserAgreementRequest:
    institution_id: str
    max_historical_days: int = 90
    access_valid_for_days: int = 90
    # https://stackoverflow.com/questions/53632152/why-cant-dataclasses-have-mutable-defaults-in-their-class-attributes-declaratio
    access_scope: List[Literal["balances", "details", "transactions"]] = field(
        default_factory=lambda: ["balances", "details", "transactions"]
    )

    def dict(self) -> dict[str, Any]:
        return asdict(self)
