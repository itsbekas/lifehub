from typing import TYPE_CHECKING, Any, Optional, Type

from sqlalchemy import select
from sqlalchemy.orm import Session

from lifehub.core.common.base.pagination import PaginatedRequest, PaginatedResponse
from lifehub.core.common.base.repository.base import BaseRepository
from lifehub.core.user.schema import User

if TYPE_CHECKING:
    from typing import Tuple

    from sqlalchemy import Select

    from lifehub.core.common.base.repository import UserBaseModelType


class UserBaseRepository(BaseRepository[UserBaseModelType]):
    def __init__(self, model: Type[UserBaseModelType], user: User, session: Session):
        super().__init__(model, session)
        self.user: User = user

    @property
    def base_query(self) -> Select[Tuple[UserBaseModelType]]:
        """Base query for the repository, filtered by user_id."""
        return select(self.model).where(self.model.user_id == self.user.id)

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
        return self.session.execute(self.base_query).scalar_one_or_none()

    def get_all(self) -> list[UserBaseModelType]:
        return list(self.session.execute(self.base_query).scalars().all())

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
        # Make sure query respects base_query, which can be different for each sub-class
        return super().get_paginated(request, query or self.base_query)

    def update(self, obj: UserBaseModelType) -> None:
        if obj.user_id == self.user.id:
            super().update(obj)
        raise ValueError("User ID does not match")

    def delete(self, obj: UserBaseModelType) -> None:
        if obj.user_id == self.user.id:
            super().delete(obj)
        raise ValueError("User ID does not match")
