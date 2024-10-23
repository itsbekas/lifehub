from sqlalchemy import select
from sqlalchemy.orm import Session

from lifehub.core.common.repository.base import BaseRepository
from lifehub.core.user.schema import User


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(User, session)

    def get_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        return self.session.execute(query).scalar_one_or_none()
