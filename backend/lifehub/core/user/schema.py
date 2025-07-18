import datetime as dt
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lifehub.core.common.base.db_model import BaseModel
from lifehub.core.security.encrypted_data import EncryptedDataType

if TYPE_CHECKING:
    from lifehub.core.provider.schema import Provider, ProviderToken
    from lifehub.modules.finance.schema import BankAccount, BudgetCategory


class User(BaseModel):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    email: Mapped[bytes] = mapped_column(
        EncryptedDataType(64), unique=True, nullable=False
    )
    email_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    name: Mapped[bytes] = mapped_column(EncryptedDataType(64))
    created_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now)
    verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    data_key: Mapped[str] = mapped_column(String(256), nullable=True)

    providers: Mapped[list["Provider"]] = relationship(
        secondary="provider_token",
        back_populates="users",
        primaryjoin="User.id == ProviderToken.user_id",
        secondaryjoin="Provider.id == ProviderToken.provider_id",
        viewonly=True,
    )
    provider_tokens: Mapped[list["ProviderToken"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    bank_accounts: Mapped[list["BankAccount"]] = relationship(
        cascade="all, delete-orphan"
    )
    budget_categories: Mapped[list["BudgetCategory"]] = relationship(
        cascade="all, delete-orphan"
    )
