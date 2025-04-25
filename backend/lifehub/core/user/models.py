import datetime as dt

from pydantic.dataclasses import dataclass


@dataclass
class UserLoginRequest:
    username: str
    password: str


@dataclass
class UserCreateRequest:
    username: str
    email: str
    password: str
    name: str


@dataclass
class UserVerifyRequest:
    token: str


@dataclass
class UserTokenResponse:
    name: str
    access_token: str
    expires_at: dt.datetime


@dataclass
class UserResponse:
    id: str
    username: str
    email: str
    name: str
    created_at: dt.datetime
    verified: bool
    is_admin: bool


@dataclass
class UpdateUserRequest:
    name: str | None = None
    email: str | None = None
    password: str | None = None
