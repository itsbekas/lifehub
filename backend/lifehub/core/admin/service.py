from sqlalchemy.orm import Session

from lifehub.core.common.base.service.base import BaseService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.security.encryption import EncryptionService
from lifehub.core.user.models import UserResponse
from lifehub.core.user.repository.user import UserRepository


class AdminServiceException(ServiceException):
    def __init__(self, status_code: int, message: str):
        super().__init__("Admin", status_code, message)


class AdminService(BaseService):
    def __init__(self, session: Session) -> None:
        super().__init__(session)
        self.user_repository = UserRepository(self.session)

    def get_all_users(self) -> list[UserResponse]:
        """Get all users. For admin use only."""
        users = self.user_repository.get_all()
        user_list = []
        for user in users:
            encryption_service = EncryptionService(self.session, user)
            user_list.append(
                UserResponse(
                    username=user.username,
                    email=encryption_service.decrypt_data(user.email),
                    name=encryption_service.decrypt_data(user.name),
                    created_at=user.created_at,
                    verified=user.verified,
                    is_admin=user.is_admin,
                )
            )

        return user_list
