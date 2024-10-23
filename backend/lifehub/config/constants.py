import os

from dotenv import load_dotenv

load_dotenv()

err = NotImplementedError


def getenv(key: str) -> str:
    if (val := os.getenv(key)) is None:
        raise NotImplementedError(f"{key} is not set")
    return val


UVICORN_HOST = getenv("UVICORN_HOST")
REDIRECT_URI_BASE = getenv("FRONTEND_URL")
OAUTH_REDIRECT_URI = f"{REDIRECT_URI_BASE}/settings/providers/oauth_token"

AUTH_SECRET_KEY = getenv("AUTH_SECRET_KEY")
AUTH_ALGORITHM = getenv("AUTH_ALGORITHM")

DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_NAME = getenv("DB_NAME")
DATABASE_URL = (
    f"mariadb+mariadbconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"
)

POSTMARK_API_TOKEN = getenv("POSTMARK_API_TOKEN")

__all__ = [
    "UVICORN_HOST",
    "REDIRECT_URI_BASE",
    "AUTH_SECRET_KEY",
    "AUTH_ALGORITHM",
    "DATABASE_URL",
    "POSTMARK_API_TOKEN",
]
