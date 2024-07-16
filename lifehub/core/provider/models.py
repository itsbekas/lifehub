from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class ProviderResponse:
    id: int
    name: str
    allow_custom_url: bool


from lifehub.core.module.models import ModuleResponse  # noqa: E402


@dataclass
class ProviderWithModulesResponse:
    id: int
    name: str
    type: str
    allow_custom_url: bool
    modules: list[ModuleResponse]


@dataclass
class ProviderTokenTokenRequest:
    token: str
    custom_url: Optional[str] = None


@dataclass
class ProviderTokenBasicRequest:
    username: str
    password: str
    custom_url: Optional[str] = None
