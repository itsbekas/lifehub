import datetime as dt
from typing import TYPE_CHECKING, List

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lifehub.core.common.base_model import BaseModel
from lifehub.core.user.schema import user_module

if TYPE_CHECKING:
    from lifehub.core.provider.schema import Provider
    from lifehub.core.user.schema import User


module_provider = Table(
    "module_provider",
    BaseModel.metadata,
    Column("module_id", ForeignKey("module.id"), primary_key=True),
    Column("provider_id", ForeignKey("provider.id"), primary_key=True),
)


class Module(BaseModel):
    __tablename__ = "module"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
    last_update: Mapped[dt.datetime] = mapped_column(insert_default=dt.datetime.min)

    providers: Mapped[List["Provider"]] = relationship(
        secondary=module_provider, back_populates="modules"
    )

    users: Mapped[List["User"]] = relationship(
        secondary=user_module, back_populates="modules"
    )
