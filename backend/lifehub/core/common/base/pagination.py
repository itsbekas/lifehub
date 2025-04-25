from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, List, Sequence, TypeVar

from pydantic.dataclasses import dataclass as pydantic_dataclass
from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

T = TypeVar("T")


@pydantic_dataclass
class PaginatedRequest:
    """Base class for paginated requests.

    This class can be extended by other request models to add pagination parameters.
    """

    page: int = 1
    page_size: int = 20

    def __post_init__(self) -> None:
        # Ensure page and page_size are valid
        if self.page < 1:
            self.page = 1
        if self.page_size < 1:
            self.page_size = 20
        if self.page_size > 100:
            self.page_size = 100

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
    has_next: bool
    has_prev: bool

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
            has_next=request.page < total_pages,
            has_prev=request.page > 1,
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
    session: Session,
    query: Select[Any],
    request: PaginatedRequest,
    count_column: Any = None,
) -> tuple[Sequence[Any], int]:
    """
    Apply pagination to a SQLAlchemy query and return results with total count.

    Args:
        session: SQLAlchemy session
        query: SQLAlchemy select statement
        request: Pagination request with page and page_size
        count_column: Column to use for count query (defaults to first column in query)

    Returns:
        Tuple of (paginated results, total count)
    """
    # If no count column specified, use the first column in the query
    if count_column is None:
        # Extract the first entity from the query
        if hasattr(query, "column_descriptions") and query.column_descriptions:
            count_column = query.column_descriptions[0]["entity"]
        else:
            # For select() statements
            count_column = (
                query.columns[0]
                if hasattr(query, "columns") and query.columns
                else None
            )

    # Execute count query
    count_query = select(func.count()).select_from(query.subquery())
    total = session.execute(count_query).scalar() or 0

    # Apply pagination
    paginated_query = query.offset(request.offset).limit(request.limit)
    results = session.execute(paginated_query).scalars().all()

    return results, total
