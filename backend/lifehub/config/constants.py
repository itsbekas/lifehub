from __future__ import annotations

import os

import hvac
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Singleton class to store configuration constants with type hints.
    """

    __instance: Config | None = None

    # Environment
    ENVIRONMENT: str
    UVICORN_HOST: str
    REDIRECT_URI_BASE: str
    OAUTH_REDIRECT_URI: str
    AUTH_SECRET_KEY: str
    AUTH_ALGORITHM: str
    DB_HOST: str
    DB_NAME: str
    VAULT_ADDR: str
    VAULT_TOKEN: str
    VAULT_DB_USER: str
    VAULT_DB_PASSWORD: str
    VAULT_DB_ROLE: str
    VAULT_DB_ADMIN_ROLE: str
    VAULT_DB_MOUNT_POINT: str
    VAULT_TRANSIT_MOUNT_POINT: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    # Vault
    GOCARDLESS_BANK_ID: str
    GOCARDLESS_CLIENT_ID: str
    GOCARDLESS_CLIENT_SECRET: str
    POSTMARK_API_TOKEN: str
    GOOGLE_CALENDAR_CLIENT_ID: str
    GOOGLE_CALENDAR_CLIENT_SECRET: str
    GOOGLE_TASKS_CLIENT_ID: str
    GOOGLE_TASKS_CLIENT_SECRET: str
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    STRAVA_CLIENT_ID: str
    STRAVA_CLIENT_SECRET: str
    YNAB_CLIENT_ID: str
    YNAB_CLIENT_SECRET: str

    def __new__(cls) -> Config:
        if cls.__instance is None:
            cls.__instance = super(Config, cls).__new__(cls)
        return cls.__instance

    def _getenv(self, key: str) -> str:
        if (val := os.getenv(key)) is None:
            raise NotImplementedError(f"{key} is not set")
        return val

    def _load_env(self) -> None:
        """Load environment variables"""
        #
        self.ENVIRONMENT = self._getenv("ENVIRONMENT")
        self.UVICORN_HOST = self._getenv("UVICORN_HOST")
        self.REDIRECT_URI_BASE = self._getenv("FRONTEND_URL")
        self.OAUTH_REDIRECT_URI = (
            f"{self.REDIRECT_URI_BASE}/settings/providers/oauth_token"
        )
        self.AUTH_ALGORITHM = "HS256"
        self.DB_HOST = self._getenv("DB_HOST")
        self.DB_NAME = self._getenv("DB_NAME")
        self.VAULT_DB_USER = self._getenv("VAULT_DB_USER")
        self.VAULT_DB_PASSWORD = self._getenv("VAULT_DB_PASSWORD")
        self.VAULT_DB_ROLE = "lifehub-app"
        self.VAULT_DB_ADMIN_ROLE = "lifehub-admin"
        self.VAULT_DB_MOUNT_POINT = "database/lifehub"
        self.VAULT_TRANSIT_MOUNT_POINT = "transit/lifehub"
        self.ADMIN_USERNAME = self._getenv("ADMIN_USERNAME")
        self.ADMIN_PASSWORD = self._getenv("ADMIN_PASSWORD")

        # Vault
        self.VAULT_ADDR = self._getenv("VAULT_ADDR")
        self.VAULT_APPROLE_ROLE_ID = self._getenv("VAULT_APPROLE_ROLE_ID")
        self.VAULT_APPROLE_SECRET_ID = self._getenv("VAULT_APPROLE_SECRET_ID")
        self.VAULT_TOKEN = hvac.Client().auth.approle.login(
            role_id=self.VAULT_APPROLE_ROLE_ID, secret_id=self.VAULT_APPROLE_SECRET_ID
        )["auth"]["client_token"]

    def _load_vault_secrets(self) -> None:
        """Load Vault secrets"""

        vault = hvac.Client(url=self.VAULT_ADDR, token=self.VAULT_TOKEN)

        if self.ENVIRONMENT == "development":
            load_secret = self._getenv
        elif self.ENVIRONMENT == "production":

            def load_secret(key: str) -> str:
                secret: str = vault.secrets.kv.v2.read_secret_version(
                    mount_point="kv/lifehub", path=key
                )["data"]["data"]
                return secret

        # Backend Secrets
        self.AUTH_SECRET_KEY = load_secret("AUTH_SECRET_KEY")

        # Provider API Secrets
        self.GOCARDLESS_BANK_ID = load_secret("GOCARDLESS_BANK_ID")
        self.GOCARDLESS_CLIENT_ID = load_secret("GOCARDLESS_CLIENT_ID")
        self.GOCARDLESS_CLIENT_SECRET = load_secret("GOCARDLESS_CLIENT_SECRET")
        self.POSTMARK_API_TOKEN = load_secret("POSTMARK_API_TOKEN")
        self.GOOGLE_CALENDAR_CLIENT_ID = load_secret("GOOGLE_CALENDAR_CLIENT_ID")
        self.GOOGLE_CALENDAR_CLIENT_SECRET = load_secret(
            "GOOGLE_CALENDAR_CLIENT_SECRET"
        )
        self.GOOGLE_TASKS_CLIENT_ID = load_secret("GOOGLE_TASKS_CLIENT_ID")
        self.GOOGLE_TASKS_CLIENT_SECRET = load_secret("GOOGLE_TASKS_CLIENT_SECRET")
        self.SPOTIFY_CLIENT_ID = load_secret("SPOTIFY_CLIENT_ID")
        self.SPOTIFY_CLIENT_SECRET = load_secret("SPOTIFY_CLIENT_SECRET")
        self.STRAVA_CLIENT_ID = load_secret("STRAVA_CLIENT_ID")
        self.STRAVA_CLIENT_SECRET = load_secret("STRAVA_CLIENT_SECRET")
        self.YNAB_CLIENT_ID = load_secret("YNAB_CLIENT_ID")
        self.YNAB_CLIENT_SECRET = load_secret("YNAB_CLIENT_SECRET")


# Instantiate and load config once
cfg = Config()
