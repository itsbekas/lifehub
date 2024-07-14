from pydantic.dataclasses import dataclass


@dataclass
class ProviderResponse:
    id: int
    name: str


from lifehub.core.module.models import ModuleResponse  # noqa: E402


@dataclass
class ProviderWithModulesResponse:
    id: int
    name: str
    type: str
    modules: list[ModuleResponse]


@dataclass
class ProviderTokenTokenRequest:
    token: str


@dataclass
class ProviderTokenBasicRequest:
    username: str
    password: str
