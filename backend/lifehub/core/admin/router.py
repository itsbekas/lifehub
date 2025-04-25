from fastapi import APIRouter, Depends

from lifehub.core.admin.dependencies import AdminServiceDep, user_is_admin
from lifehub.core.user.models import UserResponse

router = APIRouter(dependencies=[Depends(user_is_admin)])


@router.get("/users")
async def get_users(
    admin_service: AdminServiceDep,
) -> list[UserResponse]:
    """
    Get all users with their verification status.
    """
    return admin_service.get_all_users()


@router.post("/users/{user_id}/verify")
async def verify_user(
    admin_service: AdminServiceDep,
    user_id: str,
) -> None:
    """
    Verify a user by ID.
    """
    admin_service.verify_user(user_id)
