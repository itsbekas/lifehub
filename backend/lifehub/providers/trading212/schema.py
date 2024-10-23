from decimal import Decimal

from sqlalchemy import DECIMAL, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from lifehub.core.common.base_model import FetchBaseModel


class T212Transaction(FetchBaseModel):
    __tablename__ = "t212_transaction"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))


class T212Order(FetchBaseModel):
    __tablename__ = "t212_order"

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    ticker: Mapped[str] = mapped_column(String(10))
    quantity: Mapped[Decimal] = mapped_column(DECIMAL(15, 7))
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))


class T212Balance(FetchBaseModel):
    __tablename__ = "t212_balance"

    free: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    invested: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    result: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))


class T212Dividend(FetchBaseModel):
    __tablename__ = "t212_dividend"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    ticker: Mapped[str] = mapped_column(String(10))
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    quantity: Mapped[Decimal] = mapped_column(DECIMAL(15, 7))
