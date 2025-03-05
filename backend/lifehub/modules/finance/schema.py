from __future__ import annotations

import datetime as dt
import uuid
from decimal import Decimal
from typing import Optional

from sqlalchemy import DECIMAL, UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lifehub.core.common.base.db_model import BaseModel, FetchBaseModel, UserBaseModel
from lifehub.core.security.encrypted_data import EncryptedDataType


class BankAccount(UserBaseModel):
    __tablename__ = "bank_account"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    account_id: Mapped[str] = mapped_column(EncryptedDataType)  # str
    institution_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    requisition_id: Mapped[str] = mapped_column(String(64))
    last_synced: Mapped[dt.datetime] = mapped_column(default=dt.datetime.min)

    transactions: Mapped[list[BankTransaction]] = relationship(
        back_populates="account",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    balances: Mapped[list[AccountBalance]] = relationship(
        back_populates="account", cascade="all, delete-orphan", passive_deletes=True
    )


class AccountBalance(FetchBaseModel):
    __tablename__ = "account_balance"

    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("bank_account.id", ondelete="CASCADE"),
        primary_key=True,
    )
    amount: Mapped[str] = mapped_column(EncryptedDataType)  # float / Decimal

    account: Mapped[BankAccount] = relationship(back_populates="balances")


class BankTransaction(UserBaseModel):
    __tablename__ = "bank_transaction"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    transaction_id: Mapped[str] = mapped_column(String(64))
    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("bank_account.id", ondelete="CASCADE")
    )
    amount: Mapped[str] = mapped_column(EncryptedDataType)  # float / Decimal
    date: Mapped[dt.datetime] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column(
        EncryptedDataType, nullable=True
    )  # str
    user_description: Mapped[Optional[str]] = mapped_column(
        EncryptedDataType, nullable=True, default=None
    )  # str
    counterparty: Mapped[Optional[str]] = mapped_column(
        EncryptedDataType, nullable=True
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
    name: Mapped[str] = mapped_column(String(64))

    subcategories: Mapped[list[BudgetSubCategory]] = relationship(
        back_populates="category"
    )


class BudgetSubCategory(UserBaseModel):
    __tablename__ = "budget_subcategory"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("budget_category.id")
    )
    name: Mapped[str] = mapped_column(String(64))
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))

    category: Mapped[BudgetCategory] = relationship(
        back_populates="subcategories", single_parent=True
    )


class BankTransactionFilter(UserBaseModel):
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
