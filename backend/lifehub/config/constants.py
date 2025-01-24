import os

from dotenv import load_dotenv

load_dotenv()

err = NotImplementedError


def getenv(key: str) -> str:
    if (val := os.getenv(key)) is None:
        raise NotImplementedError(f"{key} is not set")
    return val


ENVIRONMENT = getenv("ENVIRONMENT")

UVICORN_HOST = getenv("UVICORN_HOST")
REDIRECT_URI_BASE = getenv("FRONTEND_URL")
OAUTH_REDIRECT_URI = f"{REDIRECT_URI_BASE}/settings/providers/oauth_token"

AUTH_SECRET_KEY = getenv("AUTH_SECRET_KEY")
AUTH_ALGORITHM = getenv("AUTH_ALGORITHM")

DB_HOST = getenv("DB_HOST")
DB_NAME = getenv("DB_NAME")

VAULT_ADDR = getenv("VAULT_ADDR")
VAULT_TOKEN = getenv("VAULT_TOKEN")
VAULT_DB_USER = getenv("VAULT_DB_USER")
VAULT_DB_PASSWORD = getenv("VAULT_DB_PASSWORD")
VAULT_DB_ROLE = "mariadb-role"

ADMIN_USERNAME = getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = getenv("ADMIN_PASSWORD")

GOCARDLESS_BANK_ID = getenv("GOCARDLESS_BANK_ID")
GOCARDLESS_CLIENT_ID = getenv("GOCARDLESS_CLIENT_ID")
GOCARDLESS_CLIENT_SECRET = getenv("GOCARDLESS_CLIENT_SECRET")

POSTMARK_API_TOKEN = getenv("POSTMARK_API_TOKEN")

__all__ = [
    "ENVIRONMENT",
    "UVICORN_HOST",
    "REDIRECT_URI_BASE",
    "OAUTH_REDIRECT_URI",
    "AUTH_SECRET_KEY",
    "AUTH_ALGORITHM",
    "DB_HOST",
    "DB_NAME",
    "VAULT_ADDR",
    "VAULT_TOKEN",
    "VAULT_DB_USER",
    "VAULT_DB_PASSWORD",
    "VAULT_DB_ROLE",
    "ADMIN_USERNAME",
    "ADMIN_PASSWORD",
    "GOCARDLESS_BANK_ID",
    "GOCARDLESS_CLIENT_ID",
    "GOCARDLESS_CLIENT_SECRET",
    "POSTMARK_API_TOKEN",
]
