import base64 as b64
import datetime as dt

import requests
from sqlalchemy.orm import Session

from lifehub.config.constants import cfg
from lifehub.core.common.base.service.base import BaseService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.provider.models import ProviderResponse
from lifehub.core.provider.repository.provider import ProviderRepository
from lifehub.core.provider.schema import (
    BasicProviderConfig,
    OAuthProviderConfig,
    Provider,
    TokenProviderConfig,
    is_basic_config,
    is_oauth_config,
    is_token_config,
)


class ProviderServiceException(ServiceException):
    def __init__(self, status_code: int, message: str):
        super().__init__("Provider", status_code, message)


class ProviderService(BaseService):
    def __init__(self, session: Session) -> None:
        super().__init__(session)
        self.provider_repository = ProviderRepository(self.session)

    def get_provider_by_id(self, provider_id: str) -> Provider:
        provider = self.provider_repository.get_by_id(provider_id)
        if provider is None:
            raise ProviderServiceException(404, "Provider not found")
        return provider

    def get_providers(self) -> list[ProviderResponse]:
        providers = self.provider_repository.get_all()

        return [
            ProviderResponse(
                id=provider.id,
                name=provider.name,
                allow_custom_url=provider.config.allow_custom_url,
            )
            for provider in providers
        ]

    def get_provider_ids(self) -> list[str]:
        providers = self.provider_repository.get_all()

        return [provider.id for provider in providers]

    def validate_basic_provider(self, provider: Provider) -> None:
        if not is_basic_config(provider.config):
            raise ProviderServiceException(404, "Provider must be a basic login provider")

    def validate_oauth_provider(self, provider: Provider) -> None:
        if not is_oauth_config(provider.config):
            raise ProviderServiceException(404, "Provider must be an OAuth provider")

    def validate_token_provider(self, provider: Provider) -> None:
        if not is_token_config(provider.config):
            raise ProviderServiceException(404, "Provider must be a token provider")

    def get_oauth_config(self, provider: Provider) -> OAuthProviderConfig:
        if not is_oauth_config(provider.config):
            raise ProviderServiceException(404, "Provider must be an OAuth provider")
        return provider.config

    def get_token_config(self, provider: Provider) -> TokenProviderConfig:
        if not is_token_config(provider.config):
            raise ProviderServiceException(404, "Provider must be a token provider")
        return provider.config

    def get_basic_config(self, provider: Provider) -> BasicProviderConfig:
        if not is_basic_config(provider.config):
            raise ProviderServiceException(404, "Provider must be a basic login provider")
        return provider.config

    def process_oauth_token(
        self, provider: Provider, code: str
    ) -> tuple[str, str, dt.datetime, dt.datetime]:
        if not is_oauth_config(provider.config):
            raise ProviderServiceException(404, "Provider must be an OAuth provider")

        url = provider.config.build_token_url(code)
        data = {}
        params: dict[str, str] = {}
        headers = {}

        if provider.id == "spotify":
            url = provider.config.token_url
            headers = {
                "Authorization": "Basic "
                + b64.b64encode(
                    f"{provider.config.client_id}:{provider.config.client_secret}".encode(
                        "utf-8"
                    )
                ).decode("utf-8"),
                "Content-Type": "application/x-www-form-urlencoded",
            }
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": cfg.OAUTH_REDIRECT_URI,
            }

        res = requests.post(url, data=data, params=params, headers=headers)
        if res.status_code != 200:
            raise ProviderServiceException(res.status_code, res.text)

        data = res.json()
        if "created_at" in data:
            created_at = dt.datetime.fromtimestamp(float(data["created_at"]))
        else:
            created_at = dt.datetime.now()
        expires_at = created_at + dt.timedelta(seconds=float(data["expires_in"]))

        return data["access_token"], data["refresh_token"], created_at, expires_at
