from sqlalchemy import select
from sqlalchemy.orm import Session

from lifehub.core.common.repository.base import BaseRepository
from lifehub.core.provider.schema import Provider


class ProviderRepository(BaseRepository[Provider]):
    def __init__(self, session: Session):
        super().__init__(Provider, session)

    def get_by_id(self, id: str) -> Provider | None:
        stmt = select(Provider).where(Provider.id == id)
        return self.session.execute(stmt).scalar_one_or_none()
