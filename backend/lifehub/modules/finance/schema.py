import datetime as dt
import uuid
from decimal import Decimal

from sqlalchemy import DECIMAL, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from lifehub.core.common.base.db_model import BaseModel


class BankAccount(BaseModel):
    __tablename__ = "bank_account"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)
    account_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    institution_id: Mapped[str] = mapped_column(String(64), primary_key=True)


class AccountBalance(BaseModel):
    __tablename__ = "account_balance"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)
    timestamp: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.now, primary_key=True
    )
    balance: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
