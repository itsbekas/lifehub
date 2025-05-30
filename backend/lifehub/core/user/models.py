import datetime as dt

from pydantic.dataclasses import dataclass


@dataclass
class LoginUserRequest:
    username: str
    password: str


@dataclass
class CreateUserRequest:
    username: str
    email: str
    password: str
    name: str


@dataclass
class VerifyUserRequest:
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
