from __future__ import annotations

import os
from typing import Any

import hvac
import redis
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Singleton class to store configuration constants, loading from Redis.
    """

    __instance: Config | None = None
    redis_client: redis.Redis[str]

    # Type hints for IDE support
    ENVIRONMENT: str
    UVICORN_HOST: str
    REDIRECT_URI_BASE: str
    OAUTH_REDIRECT_URI: str
    AUTH_SECRET_KEY: str
    AUTH_ALGORITHM: str
    DB_HOST: str
    DB_NAME: str
    VAULT_ADDR: str
    VAULT_DB_USER: str
    VAULT_DB_ROLE: str
    VAULT_DB_ADMIN_ROLE: str
    VAULT_DB_MOUNT_POINT: str
    VAULT_TRANSIT_MOUNT_POINT: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    # Provider API Secrets
    GOCARDLESS_CLIENT_ID: str
    GOCARDLESS_CLIENT_SECRET: str
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
        """Ensure singleton instance and load from Redis on first access."""
        if cls.__instance is None:
            cls.__instance = super(Config, cls).__new__(cls)
            redis_host = cls.__instance._getenv("REDIS_HOST")
            redis_port = int(cls.__instance._getenv("REDIS_PORT"))
            cls.__instance.redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                decode_responses=True,
            )
            cls.__instance._load_from_redis()
        return cls.__instance

    def _getenv(self, key: str) -> str:
        """Retrieve environment variable or raise error if not set."""
        if (val := os.getenv(key)) is None:
            raise NotImplementedError(f"{key} is not set")
        return val

    def _load_from_redis(self) -> None:
        """Load configuration from Redis into memory."""
        if not self.redis_client.exists("config:loaded"):
            raise NotImplementedError("Redis configuration not loaded")

        config_data = self.redis_client.hgetall("config")
        for key, value in config_data.items():
            setattr(self, key, value)

    def _initialize_redis(self) -> None:
        """Initialize Redis with environment and Vault secrets (first-time setup)."""
        env_config = {
            "ENVIRONMENT": self._getenv("ENVIRONMENT"),
            "UVICORN_HOST": self._getenv("UVICORN_HOST"),
            "AUTH_ALGORITHM": "HS256",
            "DB_HOST": self._getenv("DB_HOST"),
            "DB_NAME": self._getenv("DB_NAME"),
            "VAULT_DB_USER": "vault",
            "VAULT_DB_ROLE": "lifehub-app",
            "VAULT_DB_ADMIN_ROLE": "lifehub-admin",
            "VAULT_DB_MOUNT_POINT": "database/lifehub",
            "VAULT_TRANSIT_MOUNT_POINT": "transit/lifehub",
            "ADMIN_USERNAME": "admin",
            "VAULT_ADDR": self._getenv("VAULT_ADDR"),
        }

        self.redis_client.hset("config", mapping=env_config)
        vault_secrets = self._load_vault_secrets()
        self.redis_client.set("config:loaded", "true")

    def _load_vault_secrets(self) -> dict[str, str]:
        """Load Vault secrets and store them in Redis."""
        vault = hvac.Client(url=self._getenv("VAULT_ADDR"))
        role_id = self._getenv("VAULT_APPROLE_ROLE_ID")
        secret_id = self._getenv("VAULT_APPROLE_SECRET_ID")

        VAULT_TOKEN = vault.auth.approle.login(role_id=role_id, secret_id=secret_id)[
            "auth"
        ]["client_token"]
        self.redis_client.set("vault:token", self.VAULT_TOKEN)

        def load_secret(key: str) -> dict[str, str]:
            secret: dict[str, Any] = vault.secrets.kv.v2.read_secret_version(
                mount_point="kv/lifehub", path=key
            )
            return secret["data"]["data"]  # type: ignore

        metadata = load_secret("metadata")
        api_tokens = load_secret("api-tokens")

        return {
            "AUTH_SECRET_KEY": metadata["AUTH_SECRET_KEY"],
            "ADMIN_PASSWORD": metadata["ADMIN_PASSWORD"],
            "FRONTEND_URL": metadata["FRONTEND_URL"]
            if self.ENVIRONMENT == "production"
            else metadata["FRONTEND_URL_DEV"],
            "REDIRECT_URI_BASE": metadata["FRONTEND_URL"],
            "OAUTH_REDIRECT_URI": f"{metadata['FRONTEND_URL']}/settings/providers/oauth_token",
            "GOCARDLESS_CLIENT_ID": api_tokens["GOCARDLESS_CLIENT_ID"],
            "GOCARDLESS_CLIENT_SECRET": api_tokens["GOCARDLESS_CLIENT_SECRET"],
            "GOOGLE_CALENDAR_CLIENT_ID": api_tokens["GOOGLE_CALENDAR_CLIENT_ID"],
            "GOOGLE_CALENDAR_CLIENT_SECRET": api_tokens[
                "GOOGLE_CALENDAR_CLIENT_SECRET"
            ],
            "GOOGLE_TASKS_CLIENT_ID": api_tokens["GOOGLE_TASKS_CLIENT_ID"],
            "GOOGLE_TASKS_CLIENT_SECRET": api_tokens["GOOGLE_TASKS_CLIENT_SECRET"],
            "SPOTIFY_CLIENT_ID": api_tokens["SPOTIFY_CLIENT_ID"],
            "SPOTIFY_CLIENT_SECRET": api_tokens["SPOTIFY_CLIENT_SECRET"],
            "STRAVA_CLIENT_ID": api_tokens["STRAVA_CLIENT_ID"],
            "STRAVA_CLIENT_SECRET": api_tokens["STRAVA_CLIENT_SECRET"],
            "YNAB_CLIENT_ID": api_tokens["YNAB_CLIENT_ID"],
            "YNAB_CLIENT_SECRET": api_tokens["YNAB_CLIENT_SECRET"],
        }


# Instantiate and load config once
cfg = Config()
