import os

from dotenv import load_dotenv

load_dotenv()

err = NotImplementedError


def getenv(key: str) -> str:
    if (val := os.getenv(key)) is None:
        raise NotImplementedError(f"{key} is not set")
    return val


UVICORN_HOST = getenv("UVICORN_HOST")
REDIRECT_URI_BASE = getenv("REDIRECT_URI_BASE")
OAUTH_REDIRECT_URI = f"{REDIRECT_URI_BASE}/settings/providers/oauth_token"

AUTH_SECRET_KEY = getenv("AUTH_SECRET_KEY")
AUTH_ALGORITHM = getenv("AUTH_ALGORITHM")

DATABASE_URL = getenv("DATABASE_URL")

POSTMARK_API_TOKEN = getenv("POSTMARK_API_TOKEN")

__all__ = [
    "UVICORN_HOST",
    "REDIRECT_URI_BASE",
    "AUTH_SECRET_KEY",
    "AUTH_ALGORITHM",
    "DATABASE_URL",
    "POSTMARK_API_TOKEN",
]
