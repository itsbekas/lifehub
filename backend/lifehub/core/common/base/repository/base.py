from typing import Any, Generic, Optional, Sequence, Type

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from lifehub.core.common.base.pagination import (
    PaginatedRequest,
    PaginatedResponse,
    paginate_query,
)
from lifehub.core.common.base.repository import BaseModelType


class BaseRepository(Generic[BaseModelType]):
    def __init__(self, model: Type[BaseModelType], session: Session) -> None:
        self.model: Type[BaseModelType] = model
        self.session = session

    def add(self, obj: BaseModelType) -> None:
        self.session.add(obj)

    def get_all(self) -> Sequence[BaseModelType]:
        statement = select(self.model)
        result = self.session.execute(statement)
        return result.scalars().all()

    def get_paginated(
        self, request: PaginatedRequest, query: Optional[Select[Any]] = None
    ) -> PaginatedResponse[BaseModelType]:
        """Get paginated results.

        Args:
            request: Pagination parameters
            query: Optional custom query. If not provided, selects all records from the model.

        Returns:
            Paginated response with items and pagination metadata
        """
        if query is None:
            query = select(self.model)

        items, total = paginate_query(self.session, query, request)

        return PaginatedResponse.from_request(request, list(items), total)

    def update(self, obj: BaseModelType) -> None:
        self.session.add(obj)

    def delete(self, obj: BaseModelType) -> None:
        self.session.delete(obj)

    def merge(self, obj: BaseModelType) -> BaseModelType:
        return self.session.merge(obj)

    def commit(self) -> None:
        self.session.commit()

    def refresh(self, obj: BaseModelType) -> None:
        self.session.refresh(obj)

    def flush(self) -> None:
        """Flush the current session to apply changes without committing."""
        self.session.flush()

    def rollback(self) -> None:
        self.session.rollback()

    def close(self) -> None:
        self.session.close()
