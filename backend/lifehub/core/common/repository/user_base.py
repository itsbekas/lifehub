from typing import Type

from sqlalchemy import select
from sqlalchemy.orm import Session

from lifehub.core.common.repository import UserBaseModelType
from lifehub.core.common.repository.base import BaseRepository
from lifehub.core.user.schema import User


class UserBaseRepository(BaseRepository[UserBaseModelType]):
    def __init__(self, model: Type[UserBaseModelType], user: User, session: Session):
        super().__init__(model, session)
        self.user: User = user

    def add(self, obj: UserBaseModelType) -> None:
        if obj.user_id == self.user.id:
            super().add(obj)
        else:
            raise ValueError("User ID does not match")

    def get_one_or_none(self) -> UserBaseModelType | None:
        statement = select(self.model).where(self.model.user_id == self.user.id)
        result = self.session.execute(statement)
        return result.scalar_one_or_none()

    def get_all(self) -> list[UserBaseModelType]:
        statement = select(self.model).where(self.model.user_id == self.user.id)
        result = self.session.execute(statement)
        return list(result.scalars().all())

    def update(self, obj: UserBaseModelType) -> None:
        if obj.user_id == self.user.id:
            super().update(obj)
        raise ValueError("User ID does not match")

    def delete(self, obj: UserBaseModelType) -> None:
        if obj.user_id == self.user.id:
            super().delete(obj)
        raise ValueError("User ID does not match")
