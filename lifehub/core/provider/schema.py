from __future__ import annotations

import datetime as dt
from enum import Enum
from typing import TYPE_CHECKING, TypeGuard

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lifehub.core.common.base_model import BaseModel, UserBaseModel
from lifehub.core.module.schema import module_provider
from lifehub.core.user.schema import user_provider

if TYPE_CHECKING:
    from lifehub.core.module.schema import Module
    from lifehub.core.user.schema import User

from lifehub.config.constants import OAUTH_REDIRECT_URI


def is_basic_config(config: ProviderConfig) -> TypeGuard[BasicProviderConfig]:
    return config.auth_type == ProviderType.basic


def is_token_config(config: ProviderConfig) -> TypeGuard[TokenProviderConfig]:
    return config.auth_type == ProviderType.token


def is_oauth_config(config: ProviderConfig) -> TypeGuard[OAuthProviderConfig]:
    return config.auth_type == ProviderType.oauth


class ProviderType(str, Enum):
    basic = "basic"
    token = "token"
    oauth = "oauth"


class Provider(BaseModel):
    __tablename__ = "provider"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
    last_fetch: Mapped[dt.datetime] = mapped_column(insert_default=dt.datetime.min)

    config: Mapped[ProviderConfig] = relationship(
        back_populates="provider", uselist=False
    )

    modules: Mapped[list[Module]] = relationship(
        secondary=module_provider, back_populates="providers"
    )
    users: Mapped[list[User]] = relationship(
        secondary=user_provider, back_populates="providers"
    )


class ProviderToken(UserBaseModel):
    __tablename__ = "provider_token"

    provider_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("provider.id"), primary_key=True
    )
    custom_url: Mapped[str] = mapped_column(String(64), nullable=True)
    token: Mapped[str] = mapped_column(String(256), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(256), nullable=True)
    created_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now)
    expires_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.max)

    user: Mapped[User] = relationship(back_populates="provider_tokens")


class ProviderConfig(BaseModel):
    __tablename__ = "provider_config"

    provider_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("provider.id"), primary_key=True
    )
    auth_type: Mapped[str] = mapped_column(String(8), nullable=False)
    allow_custom_url: Mapped[bool] = mapped_column(default=False)

    provider: Mapped[Provider] = relationship(
        back_populates="config", single_parent=True
    )

    __mapper_args__ = {
        "polymorphic_identity": "provider_config",
        "polymorphic_on": auth_type,
    }


class OAuthProviderConfig(ProviderConfig):
    __tablename__ = "oauth_provider_config"

    provider_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("provider_config.provider_id"), primary_key=True
    )
    auth_url: Mapped[str] = mapped_column(String(64), nullable=False)
    token_url: Mapped[str] = mapped_column(String(64), nullable=False)
    client_id: Mapped[str] = mapped_column(String(128), nullable=False)
    client_secret: Mapped[str] = mapped_column(String(128), nullable=False)
    scope: Mapped[str] = mapped_column(String(64), nullable=False)

    def build_auth_url(self) -> str:
        return f"{self.auth_url}?client_id={self.client_id}&redirect_uri={OAUTH_REDIRECT_URI}&scope={self.scope}&access_type=offline&response_type=code&state={self.provider_id}"

    def build_token_url(self, auth_code: str) -> str:
        return f"{self.token_url}?client_id={self.client_id}&redirect_uri={OAUTH_REDIRECT_URI}&scope={self.scope}&grant_type=authorization_code&client_secret={self.client_secret}&code={auth_code}"

    def build_refresh_token_url(self, refresh_token: str) -> str:
        return f"{self.token_url}?client_id={self.client_id}&redirect_uri={OAUTH_REDIRECT_URI}&scope={self.scope}&grant_type=refresh_token&client_secret={self.client_secret}&refresh_token={refresh_token}"

    __mapper_args__ = {"polymorphic_identity": "oauth"}


class TokenProviderConfig(ProviderConfig):
    __tablename__ = "token_provider_config"

    provider_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("provider_config.provider_id"), primary_key=True
    )

    __mapper_args__ = {"polymorphic_identity": "token"}


class BasicProviderConfig(ProviderConfig):
    __tablename__ = "basic_provider_config"

    provider_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("provider_config.provider_id"), primary_key=True
    )

    __mapper_args__ = {"polymorphic_identity": "basic"}
