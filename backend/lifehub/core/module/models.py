from pydantic.dataclasses import dataclass


@dataclass
class ModuleResponse:
    id: int
    name: str


from lifehub.core.provider.models import ProviderResponse  # noqa: E402


@dataclass
class ModuleWithProvidersResponse:
    id: int
    name: str
    providers: list[ProviderResponse]
