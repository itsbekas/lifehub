from typing import Annotated

from fastapi import Depends

from lifehub.core.common.api.dependencies import SessionDep
from lifehub.core.provider.schema import Provider
from lifehub.core.provider.service import ProviderService


def get_provider_service(session: SessionDep) -> ProviderService:
    return ProviderService(session)


ProviderServiceDep = Annotated[ProviderService, Depends(get_provider_service)]


def get_provider(
    provider_id: str,
    provider_service: ProviderServiceDep,
) -> Provider:
    return provider_service.get_provider_by_id(provider_id)


ProviderDep = Annotated[Provider, Depends(get_provider)]
