from __future__ import annotations

import os
from typing import Any

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
            cls.__instance._load_env()
            cls.__instance._load_vault_secrets()
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
        self.VAULT_DB_USER = "vault"
        self.VAULT_DB_ROLE = "lifehub-app"
        self.VAULT_DB_ADMIN_ROLE = "lifehub-admin"
        self.VAULT_DB_MOUNT_POINT = "database/lifehub"
        self.VAULT_TRANSIT_MOUNT_POINT = "transit/lifehub"
        self.ADMIN_USERNAME = "admin"

        # Vault
        self.VAULT_ADDR = self._getenv("VAULT_ADDR")
        self.VAULT_APPROLE_ROLE_ID = self._getenv("VAULT_APPROLE_ROLE_ID")
        self.VAULT_APPROLE_SECRET_ID = self._getenv("VAULT_APPROLE_SECRET_ID")

    def _load_vault_secrets(self) -> None:
        """Load Vault secrets"""
        self.VAULT_TOKEN = hvac.Client().auth.approle.login(
            role_id=self.VAULT_APPROLE_ROLE_ID, secret_id=self.VAULT_APPROLE_SECRET_ID
        )["auth"]["client_token"]

        vault = hvac.Client(url=self.VAULT_ADDR, token=self.VAULT_TOKEN)

        if self.ENVIRONMENT == "development":
            kv_mount = "kv/lifehub-dev"
        elif self.ENVIRONMENT == "production":
            kv_mount = "kv/lifehub"
        else:
            raise NotImplementedError(f"Environment {self.ENVIRONMENT} not supported")

        def load_secret(key: str) -> str:
            secret: dict[str, Any] = vault.secrets.kv.v2.read_secret_version(
                mount_point=kv_mount, path=key
            )
            return secret['data']['data']

        # Lifehub Metadata
        metadata = load_secret("metadata")
        self.AUTH_SECRET_KEY = metadata["AUTH_SECRET_KEY"]
        self.ADMIN_PASSWORD = metadata["ADMIN_PASSWORD"]

        # Provider API Secrets
        api_tokens = load_secret("api-tokens")
        self.GOCARDLESS_CLIENT_ID = api_tokens["GOCARDLESS_CLIENT_ID"]
        self.GOCARDLESS_CLIENT_SECRET = api_tokens["GOCARDLESS_CLIENT_SECRET"]
        self.GOOGLE_CALENDAR_CLIENT_ID = api_tokens["GOOGLE_CALENDAR_CLIENT_ID"]
        self.GOOGLE_CALENDAR_CLIENT_SECRET = api_tokens["GOOGLE_CALENDAR_CLIENT_SECRET"]
        self.GOOGLE_TASKS_CLIENT_ID = api_tokens["GOOGLE_TASKS_CLIENT_ID"]
        self.GOOGLE_TASKS_CLIENT_SECRET = api_tokens["GOOGLE_TASKS_CLIENT_SECRET"]
        self.SPOTIFY_CLIENT_ID = api_tokens["SPOTIFY_CLIENT_ID"]
        self.SPOTIFY_CLIENT_SECRET = api_tokens["SPOTIFY_CLIENT_SECRET"]
        self.STRAVA_CLIENT_ID = api_tokens["STRAVA_CLIENT_ID"]
        self.STRAVA_CLIENT_SECRET = api_tokens["STRAVA_CLIENT_SECRET"]
        self.YNAB_CLIENT_ID = api_tokens["YNAB_CLIENT_ID"]
        self.YNAB_CLIENT_SECRET = api_tokens["YNAB_CLIENT_SECRET"]


# Instantiate and load config once
cfg = Config()
