import datetime as dt
from decimal import Decimal
from typing import Optional

from sqlalchemy import DECIMAL, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from lifehub.core.common.base.db_model import FetchBaseModel, UserBaseModel


class BankAccount(UserBaseModel):
    __tablename__ = "bank_account"

    account_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    institution_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    last_synced: Mapped[dt.datetime] = mapped_column(default=dt.datetime.min)


class AccountBalance(FetchBaseModel):
    __tablename__ = "account_balance"

    account_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("bank_account.account_id"), primary_key=True
    )
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))


class BankTransaction(UserBaseModel):
    __tablename__ = "bank_transaction"

    transaction_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    account_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("bank_account.account_id"), primary_key=True
    )
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    date: Mapped[str] = mapped_column(String(64))
    description: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    counterparty: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
