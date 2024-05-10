from sqlalchemy import Session, select

from lifehub.core.common.repository.base import BaseRepository
from lifehub.core.provider.schema import Provider, ProviderToken
from lifehub.core.user.schema import User


class ProviderTokenRepository(BaseRepository[ProviderToken]):
    def __init__(self, session: Session):
        super().__init__(ProviderToken, session)

    def get(self, user: User, provider: Provider) -> ProviderToken | None:
        stmt = select(ProviderToken).where(
            ProviderToken.user_id == user.id, ProviderToken.provider_id == provider.id
        )
        return self.session.exec(stmt).one_or_none()
