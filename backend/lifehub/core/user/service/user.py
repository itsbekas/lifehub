import datetime as dt

import argon2
from hvac.exceptions import VaultError
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session

from lifehub.config.constants import cfg
from lifehub.config.providers import PROVIDER_CLIENTS
from lifehub.core.common.base.api_client import APIClient
from lifehub.core.common.base.service.base import BaseService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.provider.models import ProviderResponse
from lifehub.core.provider.repository.provider import ProviderRepository
from lifehub.core.provider.repository.provider_token import ProviderTokenRepository
from lifehub.core.provider.schema import Provider, ProviderToken
from lifehub.core.security.encryption import EncryptionService
from lifehub.core.user.models import UserResponse, UserTokenResponse
from lifehub.core.user.repository.user import UserRepository
from lifehub.core.user.schema import User


class UserServiceException(ServiceException):
    def __init__(self, status_code: int, message: str):
        super().__init__("User", status_code, message)


class UserService(BaseService):
    def __init__(self, session: Session) -> None:
        super().__init__(session)
        self.user_repository = UserRepository(self.session)
        self.provider_repository = ProviderRepository(self.session)
        self.provider_token_repository = ProviderTokenRepository(self.session)
        self.password_hasher = argon2.PasswordHasher()

    def create_user(self, username: str, email: str, password: str, name: str) -> User:
        if self.user_repository.get_by_username(username) is not None:
            raise UserServiceException(409, "User already exists")

        email_hash = EncryptionService.hmac(email.lower(), cfg.EMAIL_SECRET_KEY)

        if self.user_repository.get_by_email_hash(email_hash) is not None:
            raise UserServiceException(409, "User already exists")

        hashed_password = self.hash_password(password)

        # E-mail and name are empty until they can be encrypted
        new_user = User(
            username=username,
            email=bytes([0]),
            email_hash=email_hash,
            password=hashed_password,
            name=bytes([0]),
        )
        self.user_repository.add(new_user)
        self.session.flush()

        try:
            encryption_service = EncryptionService(self.session, new_user)
            user_dek = encryption_service.generate_encrypted_data_key()
        except VaultError:
            self.user_repository.delete(new_user)
            self.user_repository.commit()
            raise UserServiceException(500, "Failed to create user")

        new_user.data_key = user_dek
        new_user.email = encryption_service.encrypt_data(email)
        new_user.name = encryption_service.encrypt_data(name)

        self.session.commit()

        return new_user

    def create_access_token(self, user: User) -> UserTokenResponse:
        expires_at = dt.datetime.now() + dt.timedelta(days=30)

        return UserTokenResponse(
            name=str(user.id),
            access_token=self.create_jwt_token(str(user.id), expires_at),
            expires_at=expires_at,
        )

    def hash_password(self, password: str) -> str:
        return argon2.PasswordHasher().hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        try:
            return argon2.PasswordHasher().verify(hashed_password, password)
        except argon2.exceptions.VerifyMismatchError:
            return False

    def create_jwt_token(self, user_id: str, expires_at: dt.datetime) -> str:
        return jwt.encode(
            {"sub": user_id, "exp": expires_at, "iss": "Lifehub", "aud": "UserService"},
            cfg.AUTH_SECRET_KEY,
            algorithm=cfg.AUTH_ALGORITHM,
        )

    def decode_jwt_token(self, token: str) -> dict[str, str]:
        try:
            return jwt.decode(
                token,
                cfg.AUTH_SECRET_KEY,
                algorithms=[cfg.AUTH_ALGORITHM],
                audience="UserService",
                issuer="Lifehub",
                options={"verify_aud": True, "verify_iss": True},
            )
        except ExpiredSignatureError:
            raise UserServiceException(401, "Token expired")
        except JWTError as e:
            print(e)
            raise UserServiceException(401, "Invalid token")

    def login_user(self, username: str, password: str) -> User:
        user: User | None = self.user_repository.get_by_username(
            username
        ) or self.user_repository.get_by_email_hash(
            EncryptionService.hmac(username, cfg.EMAIL_SECRET_KEY)
        )

        if user is None or not self.verify_password(password, user.password):
            raise UserServiceException(401, "Invalid credentials")

        if not user.verified:
            raise UserServiceException(403, "User not verified")

        return user

    def authenticate_user(self, token: str) -> User:
        payload = self.decode_jwt_token(token)
        user_id: str | None = payload.get("sub")

        if user_id is None:
            raise UserServiceException(401, "Invalid token")

        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise UserServiceException(404, "User not found")
        if not user.verified:
            raise UserServiceException(403, "User not verified")

        return user

    def verify_user(self, token: str) -> User:
        user = self.authenticate_user(token)

        user.verified = True
        self.user_repository.commit()

        return user

    def get_user_data(self, user: User) -> UserResponse:
        encryption_service = EncryptionService(self.session, user)
        return UserResponse(
            id=str(user.id),
            username=user.username,
            email=encryption_service.decrypt_data(user.email),
            name=encryption_service.decrypt_data(user.name),
            created_at=user.created_at,
            verified=user.verified,
            is_admin=user.is_admin,
        )

    def get_user(self, username: str) -> User:
        user = self.user_repository.get_by_username(username)
        if user is None:
            raise UserServiceException(404, "User not found")
        return user

    def get_user_by_id(self, user_id: str) -> UserResponse:
        """Get a user by ID."""
        try:
            user = self.user_repository.get_by_id(user_id)
            if user is None:
                raise UserServiceException(404, "User not found")
            encryption_service = EncryptionService(self.session, user)
            return UserResponse(
                id=str(user.id),
                username=user.username,
                email=encryption_service.decrypt_data(user.email),
                name=encryption_service.decrypt_data(user.name),
                created_at=user.created_at,
                verified=user.verified,
                is_admin=user.is_admin,
            )
        except Exception as e:
            raise UserServiceException(404, f"Error retrieving user: {str(e)}")

    def update_user_verification(self, user: User) -> None:
        """Update a user's verification status. For admin use only."""
        self.user_repository.update(user)
        self.user_repository.commit()

    def update_user(
        self, user: User, name: str | None, email: str | None, password: str | None
    ) -> UserResponse:
        self.session.merge(user)

        encryption_service = EncryptionService(self.session, user)

        if name is not None:
            user.name = encryption_service.encrypt_data(name)
        if email is not None:
            user.email = encryption_service.encrypt_data(email)
        if password is not None:
            user.password = self.hash_password(password)

        self.session.commit()

        return UserResponse(
            id=str(user.id),
            username=user.username,
            email=email or encryption_service.decrypt_data(user.email),
            name=name or encryption_service.decrypt_data(user.name),
            created_at=user.created_at,
            verified=user.verified,
            is_admin=user.is_admin,
        )

    def delete_user(self, user: User) -> None:
        self.user_repository.delete(user)
        self.user_repository.commit()

    def get_user_providers(self, user: User) -> list[ProviderResponse]:
        return [
            ProviderResponse(
                id=provider.id,
                name=provider.name,
                type=provider.config.auth_type,
                allow_custom_url=provider.config.allow_custom_url,
            )
            for provider in user.providers
        ]

    def get_missing_providers(self, user: User) -> list[ProviderResponse]:
        all_providers = self.provider_repository.get_all()
        user_provider_ids = self.get_user_provider_ids(user)

        return [
            ProviderResponse(
                id=provider.id,
                name=provider.name,
                type=provider.config.auth_type,
                allow_custom_url=provider.config.allow_custom_url,
            )
            for provider in all_providers
            if provider.id not in user_provider_ids
        ]

    def get_user_provider_ids(self, user: User) -> list[str]:
        return [provider.id for provider in user.providers]

    def remove_provider_from_user(self, user: User, provider: Provider) -> None:
        token = self.provider_token_repository.get(user, provider)
        if token is None:
            raise UserServiceException(404, "Token not found")
        self.provider_token_repository.delete(token)
        self.user_repository.commit()

    def add_provider_token_to_user(
        self,
        user: User,
        provider: Provider,
        token: str,
        refresh_token: str | None,
        created_at: dt.datetime | None,
        expires_at: dt.datetime | None,
        custom_url: str | None = None,
        skip_test: bool = False,
    ) -> ProviderToken:
        user = self.session.merge(user)
        provider = self.session.merge(provider)

        if not provider.config.allow_custom_url and custom_url is not None:
            raise UserServiceException(400, "Provider does not allow custom URLs")

        if provider.config.allow_custom_url and custom_url is None:
            raise UserServiceException(400, "Custom URL is required")

        if self.provider_token_repository.get(user, provider) is not None:
            raise UserServiceException(409, "Token already exists")

        encryption_service = EncryptionService(self.session, user)

        provider_token = ProviderToken(
            user_id=user.id,
            provider_id=provider.id,
            custom_url=custom_url,
            token=encryption_service.encrypt_data(token),
            refresh_token=encryption_service.encrypt_data(refresh_token),
            created_at=created_at,
            expires_at=expires_at,
        )

        self.provider_token_repository.add(provider_token)
        self.user_repository.add(user)
        if not skip_test:
            self.test_provider_token(user, provider)
        self.session.commit()
        return provider_token

    def update_provider_token(
        self,
        user: User,
        provider: Provider,
        token: str,
        refresh_token: str | None = None,
        expires_at: dt.datetime | None = None,
        custom_url: str | None = None,
    ) -> ProviderToken:
        provider_token = self.provider_token_repository.get(user, provider)
        if provider_token is None:
            raise UserServiceException(404, "Token not found")

        if not provider.config.allow_custom_url and custom_url is not None:
            raise UserServiceException(400, "Provider does not allow custom URLs")

        encryption_service = EncryptionService(self.session, user)

        provider_token.token = encryption_service.encrypt_data(token)
        if refresh_token is not None:
            provider_token.refresh_token = encryption_service.encrypt_data(
                refresh_token
            )
        if expires_at is not None:
            provider_token.expires_at = expires_at
        if custom_url is not None:
            provider_token.custom_url = custom_url

        self.test_provider_token(user, provider)
        self.provider_token_repository.commit()
        return provider_token

    def test_provider_token(self, user: User, provider: Provider) -> None:
        provider_token = self.provider_token_repository.get(user, provider)
        if provider_token is None:
            raise UserServiceException(404, "Token not found")
        api_client: APIClient = PROVIDER_CLIENTS[provider.id](user, self.session)  # type: ignore
        if not api_client.test_connection():
            raise UserServiceException(400, "Token is invalid")

    def __del__(self) -> None:
        self.user_repository.close()
