from typing import Annotated

from fastapi import Depends, HTTPException

from lifehub.core.admin.service import AdminService
from lifehub.core.common.api.dependencies import SessionDep
from lifehub.core.user.api.dependencies import UserDep
from lifehub.core.user.schema import User


def get_admin_service(session: SessionDep) -> AdminService:
    return AdminService(session)


AdminServiceDep = Annotated[AdminService, Depends(get_admin_service)]


def get_admin_user(user: UserDep) -> User:
    """
    Dependency to check if the user is an admin.
    Raises HTTPException with 403 status code if the user is not an admin.

    Returns the user if they are an admin.
    """
    if not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required",
        )
    return user


AdminDep = Annotated[User, Depends(get_admin_user)]


def user_is_admin(user: AdminDep) -> None:
    """Dependency to ensure the user is an admin."""
    pass
