import datetime as dt
import uuid
from typing import Optional

from sqlalchemy.orm import Session

from lifehub.core.common.base.repository.base import BaseRepository
from lifehub.core.common.base.repository.user_base import UserBaseRepository
from lifehub.core.user.schema import User

from .schema import (
    BankAccount,
    BankTransaction,
    BankTransactionFilter,
    BankTransactionFilterMatch,
    BudgetCategory,
    BudgetSubCategory,
)


class BankAccountRepository(UserBaseRepository[BankAccount]):
    def __init__(self, user: User, session: Session) -> None:
        super().__init__(BankAccount, user=user, session=session)

    def get_by_id(self, account_id: uuid.UUID) -> BankAccount | None:
        return (
            self.session.query(BankAccount)
            .filter_by(user_id=self.user.id, id=account_id)
            .one_or_none()
        )


class BankTransactionRepository(BaseRepository[BankTransaction]):
    def __init__(self, session: Session):
        super().__init__(BankTransaction, session=session)

    def get_by_id(
        self, account: BankAccount, transaction_id: uuid.UUID
    ) -> BankTransaction | None:
        return (
            self.session.query(BankTransaction)
            .filter_by(account_id=account.id, id=transaction_id)
            .one_or_none()
        )

    def get_by_original_id(self, original_id: str) -> BankTransaction | None:
        """
        Get a transaction by its original ID (the ID assigned by the bank).
        """
        return (
            self.session.query(BankTransaction)
            .filter_by(transaction_id=original_id)
            .one_or_none()
        )

    def get_by_account(self, account: BankAccount) -> list[BankTransaction]:
        return (
            self.session.query(BankTransaction).filter_by(account_id=account.id).all()
        )

    def get_filtered_transactions(
        self,
        accounts: list[BankAccount],
        start_date: Optional[dt.datetime] = None,
        end_date: Optional[dt.datetime] = None,
        subcategory_id: Optional[uuid.UUID] = None,
        description: Optional[str] = None,
    ) -> list[BankTransaction]:
        """Get transactions filtered by date range, subcategory, and description.

        Args:
            accounts: List of bank accounts to filter transactions for
            start_date: Start date for filtering transactions
            end_date: End date for filtering transactions
            subcategory_id: Filter by subcategory ID
            description: Filter by user description

        Returns:
            List of filtered BankTransaction objects
        """
        account_ids = [account.id for account in accounts]

        query = self.session.query(BankTransaction).filter(
            BankTransaction.account_id.in_(account_ids),
        )

        if start_date:
            query = query.filter(BankTransaction.date >= start_date)
        if end_date:
            query = query.filter(BankTransaction.date <= end_date)
        if subcategory_id:
            query = query.filter(BankTransaction.subcategory_id == subcategory_id)
        if description:
            query = query.filter(BankTransaction.user_description == description)

        return query.all()


class BudgetCategoryRepository(UserBaseRepository[BudgetCategory]):
    def __init__(self, user: User, session: Session):
        super().__init__(BudgetCategory, user=user, session=session)

    def get_by_id(self, category_id: uuid.UUID) -> BudgetCategory | None:
        return (
            self.session.query(BudgetCategory)
            .filter_by(user_id=self.user.id, id=category_id)
            .one_or_none()
        )


class BudgetSubCategoryRepository(BaseRepository[BudgetSubCategory]):
    def __init__(self, session: Session):
        super().__init__(BudgetSubCategory, session=session)

    def get_by_id(self, subcategory_id: uuid.UUID) -> BudgetSubCategory | None:
        return (
            self.session.query(BudgetSubCategory)
            .filter_by(id=subcategory_id)
            .one_or_none()
        )


class BankTransactionFilterRepository(BaseRepository[BankTransactionFilter]):
    def __init__(self, session: Session):
        super().__init__(BankTransactionFilter, session=session)

    def get_by_id(self, filter_id: uuid.UUID) -> BankTransactionFilter | None:
        return (
            self.session.query(BankTransactionFilter)
            .filter_by(id=filter_id)
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
