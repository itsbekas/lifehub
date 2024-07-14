from sqlalchemy.orm import Session

from lifehub.core.common.base_service import BaseService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.module.models import ModuleResponse
from lifehub.core.provider.models import ProviderResponse, ProviderWithModulesResponse
from lifehub.core.provider.repository.provider import ProviderRepository
from lifehub.core.provider.schema import Provider


class ProviderServiceException(ServiceException):
    def __init__(self, message: str):
        super().__init__("Provider", message)


class ProviderService(BaseService):
    def __init__(self, session: Session) -> None:
        super().__init__(session)
        self.provider_repository = ProviderRepository(self.session)

    def get_provider_by_id(self, provider_id: int) -> Provider:
        provider = self.provider_repository.get_by_id(provider_id)
        if provider is None:
            raise ProviderServiceException("Provider not found")
        return provider

    def get_providers(self) -> list[ProviderResponse]:
        providers = self.provider_repository.get_all()

        return [
            ProviderResponse(
                id=provider.id,
                name=provider.name,
            )
            for provider in providers
        ]

    def get_providers_with_modules(self) -> list[ProviderWithModulesResponse]:
        providers = self.provider_repository.get_all()

        return [
            ProviderWithModulesResponse(
                id=provider.id,
                name=provider.name,
                type=provider.config.auth_type,
                modules=[
                    ModuleResponse(
                        id=module.id,
                        name=module.name,
                    )
                    for module in provider.modules
                ],
            )
            for provider in providers
        ]
