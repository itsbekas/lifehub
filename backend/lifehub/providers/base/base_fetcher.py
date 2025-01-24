import datetime as dt

from lifehub.core.common.database_service import get_session
from lifehub.core.provider.repository.provider import ProviderRepository
from lifehub.core.provider.schema import Provider
from lifehub.core.user.schema import User


class BaseFetcher:
    provider_name: str

    def __init__(self) -> None:
        with get_session() as session:
            provider: Provider | None = ProviderRepository(session).get_by_id(
                self.provider_name
            )
            if provider is None:
                raise ValueError(
                    f"Provider {self.provider_name} not found in the database"
                )
            self.provider = provider
            self.provider.users

    def _get_users(self) -> list[User]:
        return self.provider.users

    def fetch(self) -> None:
        for self.user in self._get_users():
            with get_session() as self.session:
                self.provider = self.session.merge(self.provider)
                self.fetch_data()
                self._update_fetch_timestamp()
                self.session.commit()

    def fetch_data(self) -> None:
        raise NotImplementedError("fetch_data must be implemented in the subclass")

    def _update_fetch_timestamp(self) -> None:
        self.provider.last_fetch = dt.datetime.now()

    @property
    def prev_timestamp(self) -> dt.datetime:
        return self.provider.last_fetch
