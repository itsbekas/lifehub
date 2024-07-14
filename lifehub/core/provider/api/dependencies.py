from typing import Annotated

from fastapi import Depends, HTTPException

from lifehub.core.common.api.dependencies import SessionDep
from lifehub.core.provider.schema import (
    Provider,
)
from lifehub.core.provider.service import ProviderService


def get_provider_service(session: SessionDep) -> ProviderService:
    return ProviderService(session)


ProviderServiceDep = Annotated[ProviderService, Depends(get_provider_service)]


def get_provider(
    provider_id: int,
    provider_service: ProviderServiceDep,
) -> Provider:
    provider = provider_service.get_provider_by_id(provider_id)

    if provider is None:
        raise HTTPException(404, "Provider not found")

    return provider


ProviderDep = Annotated[Provider, Depends(get_provider)]
