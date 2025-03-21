from __future__ import annotations

import os

import redis
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Singleton class to store configuration constants, loading from Redis.
    """

    __instance: Config | None = None
    redis_client: redis.Redis

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

    # Dynamic Secrets
    @property
    def VAULT_TOKEN(self) -> str:
        return self.redis_client.get("VAULT_TOKEN")  # type: ignore

    def __new__(cls) -> Config:
        """Ensure singleton instance and load from Redis on first access."""
        if cls.__instance is None:
            cls.__instance = super(Config, cls).__new__(cls)
            redis_host = cls.__instance._getenv("REDIS_HOST")
            redis_port = int(cls.__instance._getenv("REDIS_PORT"))
            redis_password = cls.__instance._getenv("REDIS_PASSWORD")
            cls.__instance.redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                decode_responses=True,
                password=redis_password,
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
            from lifehub.config.config_manager import init_config

            init_config()

        config_data = self.redis_client.hgetall("config")
        for key, value in config_data.items():  # type: ignore
            setattr(self, key, value)


# Instantiate and load config once
cfg = Config()
