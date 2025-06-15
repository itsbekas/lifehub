from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, List, Sequence, TypeVar

from pydantic import BaseModel, Field
from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

T = TypeVar("T")


class PaginatedRequest(BaseModel):
    """Base class for paginated requests.

    This class can be extended by other request models to add pagination parameters.
    """

    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

    @property
    def offset(self) -> int:
        """Calculate the offset based on page and page_size."""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Return the page_size as limit."""
        return self.page_size


@dataclass
class PaginationInfo:
    """Metadata about pagination results."""

    page: int
    page_size: int
    total_items: int
    total_pages: int

    @classmethod
    def from_request(
        cls, request: PaginatedRequest, total_items: int
    ) -> PaginationInfo:
        """Create pagination info from a request and total items count."""
        total_pages = (
            (total_items + request.page_size - 1) // request.page_size
            if total_items > 0
            else 1
        )
        return cls(
            page=request.page,
            page_size=request.page_size,
            total_items=total_items,
            total_pages=total_pages,
        )


@dataclass
class PaginatedResponse(Generic[T]):
    """Generic wrapper for paginated responses."""

    items: List[T]
    pagination: PaginationInfo

    @classmethod
    def from_request(
        cls, request: PaginatedRequest, items: List[T], total_items: int
    ) -> PaginatedResponse[T]:
        """Create a paginated response from a request, items, and total count."""
        return cls(
            items=items, pagination=PaginationInfo.from_request(request, total_items)
        )


def paginate_query(
    session: Session, query: Select[Any], request: PaginatedRequest
) -> tuple[Sequence[Any], int]:
    # Execute count query
    count_query = select(func.count()).select_from(query.subquery())
    total = session.execute(count_query).scalar() or 0

    # Apply pagination
    paginated_query = query.offset(request.offset).limit(request.limit)
    results = session.execute(paginated_query).scalars().all()

    return results, total
