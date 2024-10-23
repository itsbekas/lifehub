from sqlalchemy import select

from lifehub.core.common.repository import TimeBaseModelType
from lifehub.core.common.repository.base import BaseRepository


class TimeBaseRepository(BaseRepository[TimeBaseModelType]):
    def get_latest(self) -> TimeBaseModelType | None:
        statement = select(self.model).order_by(self.model.timestamp.desc()).limit(1)
        result = self.session.execute(statement)
        return result.scalar_one_or_none()
