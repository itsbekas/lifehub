import datetime as dt
import uuid

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    pass


class UserBaseModel(BaseModel):
    __abstract__ = True

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True
    )


class TimeBaseModel(BaseModel):
    __abstract__ = True

    timestamp: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.now, primary_key=True
    )


class FetchBaseModel(UserBaseModel, TimeBaseModel):
    __abstract__ = True
