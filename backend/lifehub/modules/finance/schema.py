from __future__ import annotations

import datetime as dt
import uuid
from decimal import Decimal
from typing import Optional

from sqlalchemy import DECIMAL, UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lifehub.core.common.base.db_model import FetchBaseModel, UserBaseModel


class BankAccount(UserBaseModel):
    __tablename__ = "bank_account"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    institution_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    requisition_id: Mapped[str] = mapped_column(String(64))
    last_synced: Mapped[dt.datetime] = mapped_column(default=dt.datetime.min)
    transactions: Mapped[list[BankTransaction]] = relationship(back_populates="account")


class AccountBalance(FetchBaseModel):
    __tablename__ = "account_balance"

    account_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("bank_account.id"), primary_key=True
    )
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))


class BankTransaction(UserBaseModel):
    __tablename__ = "bank_transaction"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    account_id: Mapped[str] = mapped_column(String(64), ForeignKey("bank_account.id"))
    account: Mapped[BankAccount] = relationship(
        back_populates="transactions", single_parent=True
    )
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    date: Mapped[dt.datetime] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    user_description: Mapped[Optional[str]] = mapped_column(
        String(256), nullable=True, default=None
    )
    counterparty: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    subcategory_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("budget_subcategory.id"), nullable=True
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
    category: Mapped[BudgetCategory] = relationship(
        back_populates="subcategories", single_parent=True
    )
    name: Mapped[str] = mapped_column(String(64))
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))


class BankTransactionFilter(UserBaseModel):
    __tablename__ = "bank_transaction_rule"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    filter: Mapped[str] = mapped_column(String(64))
    subcategory_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("budget_subcategory.id")
    )
    subcategory: Mapped[BudgetSubCategory] = relationship(single_parent=True)
    description: Mapped[str] = mapped_column(String(64))
