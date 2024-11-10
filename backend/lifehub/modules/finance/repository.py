import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from lifehub.core.common.base.repository.base import BaseRepository

from .schema import AccountBalance, BankAccount


class BankAccountRepository(BaseRepository[BankAccount]):
    def __init__(self, session: Session):
        super().__init__(BankAccount, session=session)

    def get_by_user_id(self, user_id: uuid.UUID) -> list[BankAccount]:
        query = select(BankAccount).filter(BankAccount.user_id == user_id)
        accounts = self.session.execute(query).scalars().all()
        return list(accounts)


class AccountBalanceRepository(BaseRepository[AccountBalance]):
    def __init__(self, session: Session):
        super().__init__(AccountBalance, session=session)

    def get_by_user_id(self, user_id: uuid.UUID) -> list[AccountBalance]:
        query = select(AccountBalance).filter(AccountBalance.user_id == user_id)
        balances = self.session.execute(query).scalars().all()
        return list(balances)
