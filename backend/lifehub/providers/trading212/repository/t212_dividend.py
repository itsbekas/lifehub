from sqlalchemy.orm import Session

from lifehub.core.common.repository.fetch_base import FetchBaseRepository
from lifehub.core.user.schema import User
from lifehub.providers.trading212.schema import T212Dividend


class T212DividendRepository(FetchBaseRepository[T212Dividend]):
    def __init__(self, user: User, session: Session):
        super().__init__(T212Dividend, user, session)
