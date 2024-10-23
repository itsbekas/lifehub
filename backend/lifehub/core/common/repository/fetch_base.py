from typing import Type

from sqlalchemy import select
from sqlalchemy.orm import Session

from lifehub.core.common.repository import FetchBaseModelType
from lifehub.core.common.repository.time_base import TimeBaseRepository
from lifehub.core.common.repository.user_base import UserBaseRepository
from lifehub.core.user.schema import User


class FetchBaseRepository(
    UserBaseRepository[FetchBaseModelType], TimeBaseRepository[FetchBaseModelType]
):
    def __init__(self, model: Type[FetchBaseModelType], user: User, session: Session):
        super().__init__(model, user, session)

    def get_latest(self) -> FetchBaseModelType | None:
        statement = (
            select(self.model)
            .where(self.model.user_id == self.user.id)
            .order_by(self.model.timestamp.desc())
            .limit(1)
        )
        result = self.session.execute(statement)
        return result.scalar_one_or_none()
