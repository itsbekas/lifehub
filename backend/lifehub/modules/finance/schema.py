from decimal import Decimal

from sqlalchemy import DECIMAL, String
from sqlalchemy.orm import Mapped, mapped_column

from lifehub.core.common.base.db_model import FetchBaseModel, UserBaseModel


class BankAccount(UserBaseModel):
    __tablename__ = "bank_account"

    account_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    institution_id: Mapped[str] = mapped_column(String(64), primary_key=True)


class AccountBalance(FetchBaseModel):
    __tablename__ = "account_balance"

    account_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
