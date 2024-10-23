import datetime as dt
import uuid
from decimal import Decimal

from sqlalchemy import DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from lifehub.core.common.base_model import BaseModel


class YNABBalance(BaseModel):
    __tablename__ = "ynab_balance"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)
    timestamp: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.now, primary_key=True
    )
    balance: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
