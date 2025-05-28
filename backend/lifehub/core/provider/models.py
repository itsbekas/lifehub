from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class ProviderResponse:
    id: str
    name: str
    allow_custom_url: bool


@dataclass
class UpdateProviderTokenTokenRequest:
    token: str
    custom_url: Optional[str] = None


@dataclass
class UpdateProviderTokenBasicRequest:
    username: str
    password: str
    custom_url: Optional[str] = None
