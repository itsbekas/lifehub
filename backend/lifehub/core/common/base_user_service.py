from sqlalchemy.orm import Session

from lifehub.core.common.base_service import BaseService
from lifehub.core.user.schema import User


class BaseUserService(BaseService):
    def __init__(self, session: Session, user: User) -> None:
        super().__init__(session)
        self.user: User = user
