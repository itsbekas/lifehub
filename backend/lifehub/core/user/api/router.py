from typing import Annotated

from fastapi import APIRouter, Form, HTTPException

from lifehub.core.user.api.dependencies import UserDep, UserServiceDep
from lifehub.core.user.models import (
    UpdateUserRequest,
    UserResponse,
    UserTokenResponse,
    UserVerifyRequest,
)
from lifehub.core.user.service.user import UserServiceException

router = APIRouter()


@router.post("/login")
async def user_login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    user_service: UserServiceDep,
) -> UserTokenResponse:
    try:
        user = user_service.login_user(username, password)
    except UserServiceException as e:
        raise HTTPException(status_code=401, detail=str(e))
    user_token = user_service.create_access_token(user)
    return user_token


@router.post("/signup")
async def user_signup(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    user_service: UserServiceDep,
) -> None:
    try:
        user_service.create_user(username, email, password, name)
    except UserServiceException as e:
        raise HTTPException(status_code=403, detail=str(e))


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
    token: UserVerifyRequest,
    user_service: UserServiceDep,
) -> UserTokenResponse:
    try:
        user = user_service.verify_user(token.token)
    except UserServiceException as e:
        raise HTTPException(status_code=403, detail=str(e))

    return user_service.create_access_token(user)
