import datetime as dt
import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from lifehub.core.common.base.pagination import PaginatedRequest, PaginatedResponse
from lifehub.core.common.base.repository.base import BaseRepository
from lifehub.core.common.base.repository.fetch_base import FetchBaseRepository
from lifehub.core.common.base.repository.user_base import UserBaseRepository
from lifehub.core.user.schema import User

from .schema import (
    AccountBalance,
    BankAccount,
    BankTransaction,
    BankTransactionFilter,
    BankTransactionFilterMatch,
    BudgetCategory,
    BudgetSubCategory,
)


class BankAccountRepository(UserBaseRepository[BankAccount]):
    def __init__(self, user: User, session: Session):
        super().__init__(BankAccount, user=user, session=session)


class AccountBalanceRepository(FetchBaseRepository[AccountBalance]):
    def __init__(self, user: User, session: Session):
        super().__init__(AccountBalance, user=user, session=session)

    def get_by_account_id(self, account_id: uuid.UUID) -> AccountBalance | None:
        return (
            self.session.query(AccountBalance)
            .filter_by(account_id=account_id)
            .one_or_none()
        )


class BankTransactionRepository(UserBaseRepository[BankTransaction]):
    def __init__(self, user: User, session: Session):
        super().__init__(BankTransaction, user=user, session=session)

    def get_by_id(self, transaction_id: uuid.UUID) -> BankTransaction | None:
        return (
            self.session.query(BankTransaction)
            .filter_by(user_id=self.user.id, id=transaction_id)
            .one_or_none()
        )

    def get_by_original_id(
        self, account_id: uuid.UUID, original_id: str
    ) -> BankTransaction | None:
        """
        Get a transaction by its original ID (the ID assigned by the bank).
        """
        return (
            self.session.query(BankTransaction)
            .filter_by(
                user_id=self.user.id,
                transaction_id=original_id,
                account_id=account_id,
            )
            .one_or_none()
        )

    def get_by_account_id(self, account_id: uuid.UUID) -> list[BankTransaction]:
        return (
            self.session.query(BankTransaction).filter_by(account_id=account_id).all()
        )

    def get_transactions_since(
        self, since_date: dt.datetime, subcategory_id: Optional[uuid.UUID] = None
    ) -> list[BankTransaction]:
        query = self.session.query(BankTransaction).filter(
            BankTransaction.user_id == self.user.id,
            BankTransaction.date >= since_date,
        )
        if subcategory_id:
            query = query.filter(BankTransaction.subcategory_id == subcategory_id)
        return query.all()

    def get_paginated_transactions(
        self,
        request: PaginatedRequest,
        subcategory_id: Optional[uuid.UUID] = None,
        description: Optional[str] = None,
    ) -> PaginatedResponse[BankTransaction]:
        """Get paginated transactions with optional filtering.

        Args:
            request: Pagination parameters
            subcategory_id: Filter by subcategory ID
            description: Filter by user description

        Returns:
            Paginated response with filtered transactions
        """
        # Start with a base query filtered by user_id
        query = select(BankTransaction).where(BankTransaction.user_id == self.user.id)

        # Apply subcategory filter
        if subcategory_id:
            query = query.where(BankTransaction.subcategory_id == subcategory_id)

        # Apply description filter
        if description:
            query = query.where(BankTransaction.user_description == description)

        # Order by date descending (newest first)
        query = query.order_by(BankTransaction.date.desc())

        # Use the paginated query method from the base repository
        return self.get_paginated(request, query)


class BudgetCategoryRepository(UserBaseRepository[BudgetCategory]):
    def __init__(self, user: User, session: Session):
        super().__init__(BudgetCategory, user=user, session=session)

    def get_by_id(self, category_id: uuid.UUID) -> BudgetCategory | None:
        return (
            self.session.query(BudgetCategory)
            .filter_by(user_id=self.user.id, id=category_id)
            .one_or_none()
        )


class BudgetSubCategoryRepository(UserBaseRepository[BudgetSubCategory]):
    def __init__(self, user: User, session: Session):
        super().__init__(BudgetSubCategory, user=user, session=session)

    def get_by_id(self, subcategory_id: uuid.UUID) -> BudgetSubCategory | None:
        return (
            self.session.query(BudgetSubCategory)
            .filter_by(user_id=self.user.id, id=subcategory_id)
            .one_or_none()
        )


class BankTransactionFilterRepository(UserBaseRepository[BankTransactionFilter]):
    def __init__(self, user: User, session: Session):
        super().__init__(BankTransactionFilter, user=user, session=session)

    def get_by_id(self, filter_id: uuid.UUID) -> BankTransactionFilter | None:
        return (
            self.session.query(BankTransactionFilter)
            .filter_by(user_id=self.user.id, id=filter_id)
            .one_or_none()
        )


class BankTransactionFilterMatchRepository(BaseRepository[BankTransactionFilterMatch]):
    def __init__(self, session: Session):
        super().__init__(BankTransactionFilterMatch, session=session)

    def get_by_id(self, filter_id: uuid.UUID) -> BankTransactionFilterMatch | None:
        return (
            self.session.query(BankTransactionFilterMatch)
            .filter_by(id=filter_id)
            .one_or_none()
        )
