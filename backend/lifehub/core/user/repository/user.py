import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from lifehub.core.common.base.repository.base import BaseRepository
from lifehub.core.user.schema import User


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(User, session)

    def get_by_id(self, user_id: uuid.UUID | str) -> User | None:
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        query = select(User).where(User.id == user_id)
        return self.session.execute(query).scalar_one_or_none()

    def get_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        return self.session.execute(query).scalar_one_or_none()

    def get_by_email_hash(self, email_hash: str) -> User | None:
        query = select(User).where(User.email_hash == email_hash)
        return self.session.execute(query).scalar_one_or_none()
