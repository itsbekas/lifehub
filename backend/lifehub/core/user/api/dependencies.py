from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from lifehub.core.common.api.dependencies import SessionDep
from lifehub.core.user.schema import User
from lifehub.core.user.service.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/api-login")


def get_user_service(session: SessionDep) -> UserService:
    return UserService(session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def get_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserServiceDep,
) -> User:
    return user_service.authenticate_user(token)


UserDep = Annotated[User, Depends(get_user)]


def user_is_authenticated(user: UserDep) -> None:
    pass
