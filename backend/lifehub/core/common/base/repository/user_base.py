from typing import Any, Optional, Type

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from lifehub.core.common.base.pagination import PaginatedRequest, PaginatedResponse
from lifehub.core.common.base.repository import UserBaseModelType
from lifehub.core.common.base.repository.base import BaseRepository
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
    
    def add_all(self, objs: list[UserBaseModelType]) -> None:
        for obj in objs:
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

    def get_paginated(
        self, request: PaginatedRequest, query: Optional[Select[Any]] = None
    ) -> PaginatedResponse[UserBaseModelType]:
        """Get paginated results for the current user.

        Args:
            request: Pagination parameters
            query: Optional custom query. If not provided, selects all records for the current user.

        Returns:
            Paginated response with items and pagination metadata
        """
        if query is None:
            query = select(self.model).where(self.model.user_id == self.user.id)
        else:
            # Ensure the query is filtered by user_id
            query = query.where(self.model.user_id == self.user.id)

        return super().get_paginated(request, query)

    def update(self, obj: UserBaseModelType) -> None:
        if obj.user_id == self.user.id:
            super().update(obj)
        raise ValueError("User ID does not match")

    def delete(self, obj: UserBaseModelType) -> None:
        if obj.user_id == self.user.id:
            super().delete(obj)
        raise ValueError("User ID does not match")
