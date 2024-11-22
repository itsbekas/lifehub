from sqlalchemy.orm import Session

from lifehub.core.common.base.repository.fetch_base import FetchBaseRepository
from lifehub.core.common.base.repository.user_base import UserBaseRepository
from lifehub.core.user.schema import User

from .schema import AccountBalance, BankAccount, BankTransaction


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
