from fastapi import HTTPException, status


class ProviderExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Provider already exists",
        )


class ProviderDoesNotExistException(HTTPException):
    def __init__(self, provider_name: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Provider {provider_name} does not exist",
        )


class ProviderDetailsIncompleteException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provider details are incomplete",
        )


class ProviderTypeInvalidException(HTTPException):
    def __init__(self, provider_type: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Provider type must be {provider_type}",
        )


class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )


class NoUserDataForModuleException(HTTPException):
    def __init__(self, user, module):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data for user {user} in module {module}",
        )
