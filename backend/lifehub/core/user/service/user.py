import datetime as dt

import argon2
from hvac.exceptions import VaultError
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session

from lifehub.config.constants import AUTH_ALGORITHM, AUTH_SECRET_KEY
from lifehub.config.providers import PROVIDER_CLIENTS
from lifehub.core.common.base.api_client import APIClient
from lifehub.core.common.base.service.base import BaseService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.module.models import ModuleResponse, ModuleWithProvidersResponse
from lifehub.core.module.schema import Module
from lifehub.core.provider.models import ProviderResponse, ProviderWithModulesResponse
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
        self.provider_token_repository = ProviderTokenRepository(self.session)
        self.password_hasher = argon2.PasswordHasher()

    def create_user(self, username: str, email: str, password: str, name: str) -> User:
        user = self.user_repository.get_by_username(username)

        if user is not None:
            raise UserServiceException(409, "User already exists")

        hashed_password = self.hash_password(password)

        new_user = User(
            username=username, email=email, password=hashed_password, name=name
        )
        self.user_repository.add(new_user)

        # verification_token = create_jwt_token(
        #     username, dt.datetime.now() + dt.timedelta(days=1)
        # )

        # mail_client = MailAPIClient()
        # mail_client.send_verification_email(
        #     email,
        #     name,
        #     verification_token,
        # )

        # Necessary to get the newly generated ID
        self.session.commit()
        self.user_repository.refresh(new_user)

        try:
            encryption_service = EncryptionService(self.session, new_user)
            user_dek = encryption_service.generate_encrypted_data_key()
        except VaultError:
            self.user_repository.delete(new_user)
            self.user_repository.commit()
            raise UserServiceException(500, "Failed to create user")

        new_user.data_key = user_dek

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
            AUTH_SECRET_KEY,
            algorithm=AUTH_ALGORITHM,
        )

    def decode_jwt_token(self, token: str) -> dict[str, str]:
        try:
            return jwt.decode(
                token,
                AUTH_SECRET_KEY,
                algorithms=[AUTH_ALGORITHM],
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
        user: User | None = self.user_repository.get_by_username(username)

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
        return UserResponse(
            username=user.username,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
        )

    def get_user(self, username: str) -> User:
        user = self.user_repository.get_by_username(username)
        if user is None:
            raise UserServiceException(404, "User not found")
        return user

    def update_user(
        self, user: User, name: str | None, email: str | None, password: str | None
    ) -> UserResponse:
        self.session.merge(user)

        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        if password is not None:
            user.password = self.hash_password(password)

        self.session.commit()

        return UserResponse(
            username=user.username,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
        )

    def delete_user(self, user: User) -> None:
        self.user_repository.delete(user)
        self.user_repository.commit()

    def get_user_providers(self, user: User) -> list[ProviderResponse]:
        return [
            ProviderResponse(
                id=provider.id,
                name=provider.name,
                allow_custom_url=provider.config.allow_custom_url,
            )
            for provider in user.providers
        ]

    def get_user_provider_ids(self, user: User) -> list[str]:
        return [provider.id for provider in user.providers]

    def get_user_providers_with_modules(
        self, user: User
    ) -> list[ProviderWithModulesResponse]:
        return [
            ProviderWithModulesResponse(
                id=provider.id,
                name=provider.name,
                type=provider.config.auth_type,
                allow_custom_url=provider.config.allow_custom_url,
                modules=[
                    ModuleResponse(id=module.id, name=module.name)
                    for module in provider.modules
                ],
            )
            for provider in user.providers
        ]

    def get_missing_providers_with_modules(
        self, user: User
    ) -> list[ProviderWithModulesResponse]:
        provider_repository = ProviderRepository(self.session)
        providers = provider_repository.get_all()
        user_providers = [provider.id for provider in user.providers]
        return [
            ProviderWithModulesResponse(
                id=provider.id,
                name=provider.name,
                type=provider.config.auth_type,
                allow_custom_url=provider.config.allow_custom_url,
                modules=[
                    ModuleResponse(id=module.id, name=module.name)
                    for module in provider.modules
                ],
            )
            for provider in providers
            if provider.id not in user_providers
        ]

    def add_provider_to_user(self, user: User, provider: Provider) -> None:
        user.providers.append(provider)
        self.user_repository.commit()

    def remove_provider_from_user(self, user: User, provider: Provider) -> None:
        token = self.provider_token_repository.get(user, provider)
        if token is None:
            raise UserServiceException(404, "Token not found")
        self.provider_token_repository.delete(token)
        user.providers.remove(provider)
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

        provider_token = ProviderToken(
            user_id=user.id,
            provider_id=provider.id,
            custom_url=custom_url,
            token=token,
            refresh_token=refresh_token,
            created_at=created_at,
            expires_at=expires_at,
        )

        self.provider_token_repository.add(provider_token)
        user.providers.append(provider)
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

        provider_token.token = token
        if refresh_token is not None:
            provider_token.refresh_token = refresh_token
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

    def get_user_modules(self, user: User) -> list[ModuleResponse]:
        return [
            ModuleResponse(id=module.id, name=module.name) for module in user.modules
        ]

    def get_user_modules_with_providers(
        self, user: User
    ) -> list[ModuleWithProvidersResponse]:
        return [
            ModuleWithProvidersResponse(
                id=module.id,
                name=module.name,
                providers=[
                    ProviderResponse(
                        id=provider.id,
                        name=provider.name,
                        allow_custom_url=provider.config.allow_custom_url,
                    )
                    for provider in module.providers
                ],
            )
            for module in user.modules
        ]

    def add_module_to_user(self, user: User, module: Module) -> None:
        if module in user.modules:
            raise UserServiceException(409, "Module already added to user")

        missed_providers = []

        module = self.session.merge(module)
        user = self.session.merge(user)

        for provider in module.providers:
            if provider not in user.providers:
                missed_providers.append(provider.name)

        if missed_providers:
            raise UserServiceException(
                409, f"User is missing providers: {', '.join(missed_providers)}"
            )

        user.modules.append(module)
        self.user_repository.commit()

    def remove_module_from_user(self, user: User, module: Module) -> None:
        user = self.session.merge(user)
        module = self.session.merge(module)

        if module not in user.modules:
            raise UserServiceException(404, f"User does not have module {module.name}")

        user.modules.remove(module)
        self.user_repository.commit()

    def __del__(self) -> None:
        self.user_repository.close()
