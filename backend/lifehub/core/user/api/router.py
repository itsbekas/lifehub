from fastapi import APIRouter, HTTPException

from lifehub.core.user.api.dependencies import UserDep, UserServiceDep
from lifehub.core.user.models import (
    UpdateUserRequest,
    UserCreateRequest,
    UserLoginRequest,
    UserResponse,
    UserTokenResponse,
    UserVerifyRequest,
)
from lifehub.core.user.service.user import UserServiceException

router = APIRouter()


@router.post("/login")
async def user_login(
    user_data: UserLoginRequest,
    user_service: UserServiceDep,
) -> UserTokenResponse:
    try:
        user = user_service.login_user(user_data.username, user_data.password)
    except UserServiceException as e:
        raise HTTPException(status_code=401, detail=str(e))
    user_token = user_service.create_access_token(user)
    return user_token


@router.post("/signup")
async def user_signup(
    user_data: UserCreateRequest,
    user_service: UserServiceDep,
) -> None:
    try:
        user_service.create_user(user_data.username, user_data.email, user_data.password, user_data.name)
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
