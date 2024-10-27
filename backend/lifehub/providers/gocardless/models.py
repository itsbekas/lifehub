from __future__ import annotations

from dataclasses import field
from typing import List, Literal

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


@dataclass
class EndUserAgreementRequest:
    institution_id: str
    max_historical_days: int = 90
    access_valid_for_days: int = 90
    # https://stackoverflow.com/questions/53632152/why-cant-dataclasses-have-mutable-defaults-in-their-class-attributes-declaratio
    access_scope: List[Literal["balances", "details", "transactions"]] = field(
        default_factory=lambda: ["balances", "details", "transactions"]
    )


@dataclass
class JWTObtainPairRequest:
    secret_id: str
    secret_key: str


@dataclass
class SpectacularJWTObtainResponse:
    access: str
    access_expires: int
    refresh: str
    refresh_expires: int


@dataclass
class JWTRefreshRequest:
    refresh: str


@dataclass
class SpectacularJWTRefreshResponse:
    access: str
    access_expires: int
