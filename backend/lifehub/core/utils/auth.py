import datetime as dt

import argon2
from jose import jwt

from lifehub.config.constants import AUTH_ALGORITHM, AUTH_SECRET_KEY


def hash_password(password: str) -> str:
    return argon2.PasswordHasher().hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return argon2.PasswordHasher().verify(hashed_password, password)
    except argon2.exceptions.VerifyMismatchError:
        return False


def create_jwt_token(username: str, expires_at: dt.datetime) -> str:
    return jwt.encode(
        {"sub": username, "exp": expires_at}, AUTH_SECRET_KEY, algorithm=AUTH_ALGORITHM
    )


def decode_jwt_token(token: str) -> dict[str, str]:
    return jwt.decode(token, AUTH_SECRET_KEY, algorithms=[AUTH_ALGORITHM])
