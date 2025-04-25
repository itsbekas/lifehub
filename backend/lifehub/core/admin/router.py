from fastapi import APIRouter, Depends

from lifehub.core.admin.dependencies import AdminServiceDep, user_is_admin
from lifehub.core.user.models import UserResponse

router = APIRouter(
    dependencies=[Depends(user_is_admin)],
    prefix="/admin",
    tags=["admin"],
)


@router.get("/users")
async def get_users(
    admin_service: AdminServiceDep,
) -> list[UserResponse]:
    """
    Get all users with their verification status.
    Only accessible to admin users.
    """
    return admin_service.get_all_users()
