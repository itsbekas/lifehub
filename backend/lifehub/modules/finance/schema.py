from __future__ import annotations

import datetime as dt
import uuid
from typing import Optional

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lifehub.core.common.base.db_model import BaseModel, UserBaseModel
from lifehub.core.security.encrypted_data import EncryptedDataType


class BankAccount(UserBaseModel):
    __tablename__ = "bank_account"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    account_id: Mapped[bytes] = mapped_column(EncryptedDataType(64))  # str
    institution_id: Mapped[bytes] = mapped_column(
        EncryptedDataType(64), primary_key=True
    )
    requisition_id: Mapped[bytes] = mapped_column(EncryptedDataType(64))
    last_synced: Mapped[dt.datetime] = mapped_column(default=dt.datetime.min)

    transactions: Mapped[list[BankTransaction]] = relationship(
        back_populates="account",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    balance: Mapped[AccountBalance] = relationship(
        back_populates="account", uselist=False, cascade="all, delete-orphan"
    )
    monthly_summaries: Mapped[list[MonthlySummary]] = relationship(
        back_populates="account", cascade="all, delete-orphan", passive_deletes=True
    )

    def synced_before(
        self,
        weeks: int = 0,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        milliseconds: int = 0,
        microseconds: int = 0,
    ) -> bool:
        return self.last_synced < dt.datetime.now() - dt.timedelta(
            weeks=weeks,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            milliseconds=milliseconds,
            microseconds=microseconds,
        )


class AccountBalance(BaseModel):
    __tablename__ = "account_balance"

    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("bank_account.id", ondelete="CASCADE"),
        primary_key=True,
    )
    amount: Mapped[bytes] = mapped_column(EncryptedDataType(64))  # float / Decimal
    account: Mapped[BankAccount] = relationship(back_populates="balance")


class MonthlySummary(BaseModel):
    __tablename__ = "monthly_summary"

    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("bank_account.id", ondelete="CASCADE"),
        primary_key=True,
    )
    year: Mapped[int] = mapped_column(primary_key=True)
    month: Mapped[int] = mapped_column(primary_key=True)
    income: Mapped[bytes] = mapped_column(EncryptedDataType(64))  # float / Decimal
    expenses: Mapped[bytes] = mapped_column(EncryptedDataType(64))  # float / Decimal
    balance: Mapped[bytes] = mapped_column(EncryptedDataType(64))  # float / Decimal

    account: Mapped[BankAccount] = relationship(single_parent=True)


class BankTransaction(BaseModel):
    __tablename__ = "bank_transaction"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    transaction_id: Mapped[str] = mapped_column(String(64))
    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("bank_account.id", ondelete="CASCADE"),
        index=True,
    )
    amount: Mapped[bytes] = mapped_column(EncryptedDataType(64))  # float / Decimal
    date: Mapped[dt.datetime] = mapped_column()
    description: Mapped[Optional[bytes]] = mapped_column(
        EncryptedDataType(560), nullable=True
    )  # str
    user_description: Mapped[Optional[bytes]] = mapped_column(
        EncryptedDataType(128), nullable=True, default=None
    )  # str
    counterparty: Mapped[Optional[bytes]] = mapped_column(
        EncryptedDataType(176), nullable=True
    )  # str
    subcategory_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("budget_subcategory.id"), nullable=True
    )

    account: Mapped[BankAccount] = relationship(
        back_populates="transactions", single_parent=True
    )
    subcategory: Mapped[BudgetSubCategory] = relationship(single_parent=True)


class BudgetCategory(UserBaseModel):
    __tablename__ = "budget_category"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[bytes] = mapped_column(EncryptedDataType(64))

    subcategories: Mapped[list[BudgetSubCategory]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )


class BudgetSubCategory(BaseModel):
    __tablename__ = "budget_subcategory"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("budget_category.id", ondelete="CASCADE")
    )
    name: Mapped[bytes] = mapped_column(EncryptedDataType(64))
    amount: Mapped[bytes] = mapped_column(EncryptedDataType(64))  # float / Decimal

    category: Mapped[BudgetCategory] = relationship(
        back_populates="subcategories", single_parent=True
    )


class BankTransactionFilter(BaseModel):
    __tablename__ = "bank_transaction_rule"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    description: Mapped[str] = mapped_column(String(64), nullable=True)
    subcategory_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("budget_subcategory.id"), nullable=True
    )

    subcategory: Mapped[BudgetSubCategory] = relationship(single_parent=True)
    matches: Mapped[list[BankTransactionFilterMatch]] = relationship(
        back_populates="filter", single_parent=True
    )


class BankTransactionFilterMatch(BaseModel):
    __tablename__ = "bank_transaction_rule_match"

    filter_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("bank_transaction_rule.id"), primary_key=True
    )
    match_string: Mapped[str] = mapped_column(String(64), primary_key=True)

    filter: Mapped[BankTransactionFilter] = relationship(back_populates="matches")
