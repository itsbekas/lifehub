from __future__ import annotations

from dataclasses import field
from typing import Literal, Optional

from pydantic.dataclasses import dataclass


@dataclass
class RequisitionRequest:
    redirect: str
    institution_id: str
    agreement: Optional[str] = None
    reference: Optional[str] = None
    user_language: Optional[str] = None
    ssn: Optional[str] = None
    account_selection: bool = False
    redirect_immediate: bool = False


@dataclass
class EndUserAgreementRequest:
    institution_id: str
    max_historical_days: int = 90
    access_valid_for_days: int = 90
    # https://stackoverflow.com/questions/53632152/why-cant-dataclasses-have-mutable-defaults-in-their-class-attributes-declaratio
    access_scope: list[Literal["balances", "details", "transactions"]] = field(
        default_factory=lambda: ["balances", "details", "transactions"]
    )


@dataclass
class EndUserAcceptanceDetailsRequest:
    user_agent: str
    ip_address: str


@dataclass
class EndUserAgreementResponse:
    id: str
    created: str
    institution_id: str
    max_historical_days: int
    access_valid_for_days: int
    access_scope: list[Literal["balances", "details", "transactions"]]
    accepted: Optional[str]


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


@dataclass
class SpectacularRequisitionResponse:
    id: str
    created: str
    redirect: str
    status: str
    institution_id: str
    agreement: str
    reference: str
    accounts: list[str]
    link: str
    ssn: Optional[str]
    account_selection: bool
    redirect_immediate: bool
    user_language: Optional[str] = None


@dataclass
class RequisitionsRequest:
    limit: int
    offset: int


@dataclass
class InstitutionsRequest:
    access_scopes_supported: Optional[bool] = None
    account_selection_supported: Optional[bool] = None
    business_accounts_supported: Optional[bool] = None
    card_accounts_supported: Optional[bool] = None
    corporate_accounts_supported: Optional[bool] = None
    country: Optional[str] = None
    payment_submission_supported: Optional[bool] = None
    payments_enabled: Optional[bool] = None
    pending_transactions_supported: Optional[bool] = None
    private_accounts_supported: Optional[bool] = None
    read_debtor_account_supported: Optional[bool] = None
    ssn_verification_supported: Optional[bool] = None


# IntegrationRetrieve
@dataclass
class InstitutionResponse:
    id: str
    name: str
    max_access_valid_for_days: Optional[str]
    countries: list[str]
    logo = str
    supported_payments: dict[str, list[str]]
    supported_features: list[str]
    identification_codes: list[str]
    transaction_total_days: Optional[str] = "90"


@dataclass
class TransactionsRequest:
    date_from: str
    date_to: str


@dataclass
class BalanceAmount:
    amount: str
    currency: str


@dataclass
class AccountBalance:
    balanceAmount: BalanceAmount
    balanceType: str
    lastChangeDateTime: Optional[str] = None

@dataclass
class AccountBalances:
    balances: list[AccountBalance]

    @property
    def available_amount(self) -> str | None:
        return next(
            (b.balanceAmount.amount for b in self.balances if b.balanceType == "interimAvailable"),
            None,
        )