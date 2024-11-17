from __future__ import annotations

from dataclasses import field
from typing import List, Literal, Optional

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
            (
                b.balanceAmount.amount
                for b in self.balances
                if b.balanceType == "interimAvailable"
            ),
            None,
        )


@dataclass
class CurrencyExchange:
    sourceCurrency: Optional[str] = None
    exchangeRate: Optional[str] = None
    unitCurrency: Optional[str] = None
    targetCurrency: Optional[str] = None
    quotationDate: Optional[str] = None
    contractIdentification: Optional[str] = None


@dataclass
class DebtorAccount:
    iban: Optional[str] = None
    bban: Optional[str] = None
    pan: Optional[str] = None
    maskedPan: Optional[str] = None
    msisdn: Optional[str] = None
    currency: Optional[str] = None


CreditorAccount = DebtorAccount


@dataclass
class Transaction:
    transactionAmount: BalanceAmount
    transactionId: Optional[str] = None
    entryReference: Optional[str] = None
    endToEndId: Optional[str] = None
    mandateId: Optional[str] = None
    checkId: Optional[str] = None
    creditorId: Optional[str] = None
    bookingDate: Optional[str] = None
    valueDate: Optional[str] = None
    bookingDateTime: Optional[str] = None
    valueDateTime: Optional[str] = None
    currencyExchange: Optional[CurrencyExchange] = None
    creditorName: Optional[str] = None
    creditorAccount: Optional[CreditorAccount] = None
    ultimateCreditor: Optional[str] = None
    debtorName: Optional[str] = None
    debtorAccount: Optional[DebtorAccount] = None
    ultimateDebtor: Optional[str] = None
    remittanceInformationUnstructured: Optional[str] = None
    remittanceInformationUnstructuredArray: Optional[list[str]] = None
    remittanceInformationStructured: Optional[str] = None
    remittanceInformationStructuredArray: Optional[list[str]] = None
    additionalInformation: Optional[str] = None
    purposeCode: Optional[str] = None
    bankTransactionCode: Optional[str] = None
    proprietaryBankTransactionCode: Optional[str] = None
    internalTransactionId: Optional[str] = None


@dataclass
class TransactionsResponse:
    booked: list[Transaction]
    pending: List[Transaction] = field(default_factory=list)


@dataclass
class TransactionsRequest:
    date_from: Optional[str] = None  # format: YYYY-MM-DD
    date_to: Optional[str] = None  # format: YYYY-MM-DD
