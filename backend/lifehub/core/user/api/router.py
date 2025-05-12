from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from lifehub.core.user.api.dependencies import UserDep, UserServiceDep
from lifehub.core.user.models import (
    CreateUserRequest,
    LoginUserRequest,
    UpdateUserRequest,
    UserResponse,
    UserTokenResponse,
    VerifyUserRequest,
)

router = APIRouter()


# Used to login in the Swagger UI
@router.post("/api-login")
async def user_api_login(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserServiceDep,
) -> UserTokenResponse:
    user = user_service.login_user(user_data.username, user_data.password)
    user_token = user_service.create_access_token(user)
    return user_token


# Used to login in the frontend
@router.post("/login")
async def user_login(
    user_data: LoginUserRequest,
    user_service: UserServiceDep,
) -> UserTokenResponse:
    user = user_service.login_user(user_data.username, user_data.password)
    user_token = user_service.create_access_token(user)
    return user_token


@router.post("/signup")
async def user_signup(
    user_data: CreateUserRequest,
    user_service: UserServiceDep,
) -> None:
    user_service.create_user(
        user_data.username, user_data.email, user_data.password, user_data.name
    )


@router.get("/me")
async def get_user(user: UserDep, user_service: UserServiceDep) -> UserResponse:
    return user_service.get_user_data(user)


@router.patch("/me")
async def update_user(
    user: UserDep,
    user_service: UserServiceDep,
    user_data: UpdateUserRequest,
) -> UserResponse:
    return user_service.update_user(
        user, user_data.name, user_data.email, user_data.password
    )


@router.delete("/me")
async def delete_user(user: UserDep, user_service: UserServiceDep) -> None:
    user_service.delete_user(user)


@router.post("/verify-email")
async def verify_user(
    token: VerifyUserRequest,
    user_service: UserServiceDep,
) -> UserTokenResponse:
    user = user_service.verify_user(token.token)
    return user_service.create_access_token(user)
