import datetime as dt
import uuid
from typing import Optional

from sqlalchemy.orm import Session

from lifehub.core.common.base.repository.fetch_base import FetchBaseRepository
from lifehub.core.common.base.repository.user_base import UserBaseRepository
from lifehub.core.user.schema import User

from .schema import (
    AccountBalance,
    BankAccount,
    BankTransaction,
    BudgetCategory,
    BudgetSubCategory,
)


class BankAccountRepository(UserBaseRepository[BankAccount]):
    def __init__(self, user: User, session: Session):
        super().__init__(BankAccount, user=user, session=session)


class AccountBalanceRepository(FetchBaseRepository[AccountBalance]):
    def __init__(self, user: User, session: Session):
        super().__init__(AccountBalance, user=user, session=session)

    def get_by_account_id(self, account_id: str) -> AccountBalance | None:
        return (
            self.session.query(AccountBalance)
            .filter_by(account_id=account_id)
            .one_or_none()
        )


class BankTransactionRepository(UserBaseRepository[BankTransaction]):
    def __init__(self, user: User, session: Session):
        super().__init__(BankTransaction, user=user, session=session)

    def get_by_id(self, account_id: str, transaction_id: str) -> BankTransaction | None:
        return (
            self.session.query(BankTransaction)
            .filter_by(
                user_id=self.user.id,
                id=transaction_id,
                account_id=account_id,
            )
            .one_or_none()
        )

    def get_by_account_id(self, account_id: str) -> list[BankTransaction]:
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
