from sqlalchemy.orm import Session

from lifehub.core.common.repository.fetch_base import FetchBaseRepository
from lifehub.core.user.schema import User
from lifehub.providers.trading212.schema import T212Balance


class T212BalanceRepository(FetchBaseRepository[T212Balance]):
    def __init__(self, user: User, session: Session):
        super().__init__(T212Balance, user, session)
