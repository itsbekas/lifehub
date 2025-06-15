from __future__ import annotations

import datetime as dt
import uuid

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    pass


class UserBaseModel(BaseModel):
    __abstract__ = True

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )


class TimeBaseModel(BaseModel):
    __abstract__ = True

    timestamp: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.now, primary_key=True
    )

    def older_than(
        self,
        weeks: int = 0,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        milliseconds: int = 0,
        microseconds: int = 0,
    ) -> bool:
        return self.timestamp < dt.datetime.now() - dt.timedelta(
            weeks=weeks,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            milliseconds=milliseconds,
            microseconds=microseconds,
        )
