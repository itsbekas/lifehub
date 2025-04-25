import os
import threading
import time
from typing import Any

import hvac
import redis


class ConfigManager:
    vault_client: hvac.Client
    redis_client: redis.Redis

    def __init__(self) -> None:
        redis_host = os.getenv("REDIS_HOST")
        redis_port = os.getenv("REDIS_PORT")
        redis_password = os.getenv("REDIS_PASSWORD")
        if redis_host is None or redis_port is None or redis_password is None:
            raise NotImplementedError("Redis configuration is not set")

        self.redis_client = redis.Redis(
            host=redis_host,
            port=int(redis_port),
            decode_responses=True,
            password=redis_password,
        )

    def init(self) -> None:
        """Initialize configuration for the application."""
        # This should only run once anyways but we check just in case
        if not self.redis_client.exists("config:loaded"):
            self._initialize_redis()
            threading.Thread(target=self._renew_vault_token, daemon=True).start()

    def _renew_vault_token(self) -> None:
        """Renew the Vault token every 10 minutes."""
        while True:
            r = self.vault_client.auth.token.renew_self()
            vault_token = r["auth"]["client_token"]
            self.redis_client.set("VAULT_TOKEN", vault_token)
            time.sleep(600)

    def _getenv(self, key: str) -> str:
        """Retrieve environment variable or raise error if not set."""
        if (val := os.getenv(key)) is None:
            raise NotImplementedError(f"{key} is not set")
        return val

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
        self.redis_client.hset("config", mapping=vault_secrets)
        self.redis_client.set("config:loaded", "true")

    def _load_vault_secrets(self) -> dict[str, str]:
        """Load Vault secrets and store them in Redis."""
        self.vault_client = hvac.Client(url=self._getenv("VAULT_ADDR"))
        role_id = self._getenv("VAULT_APPROLE_ROLE_ID")
        secret_id = self._getenv("VAULT_APPROLE_SECRET_ID")

        vault_token = self.vault_client.auth.approle.login(
            role_id=role_id, secret_id=secret_id
        )["auth"]["client_token"]
        self.redis_client.set("VAULT_TOKEN", vault_token)

        def load_secret(key: str) -> dict[str, str]:
            secret: dict[str, Any] = (
                self.vault_client.secrets.kv.v2.read_secret_version(
                    mount_point="kv/lifehub", path=key
                )
            )
            return secret["data"]["data"]  # type: ignore

        metadata = load_secret("metadata")
        api_tokens = load_secret("api-tokens")

        return {
            "AUTH_SECRET_KEY": metadata["AUTH_SECRET_KEY"],
            "ADMIN_PASSWORD": metadata["ADMIN_PASSWORD"],
            "FRONTEND_URL": metadata["FRONTEND_URL"],
            "REDIRECT_URI_BASE": metadata["FRONTEND_URL"],
            "OAUTH_REDIRECT_URI": f"{metadata['FRONTEND_URL']}/settings/providers/oauth_token",
            "EMAIL_SECRET_KEY": metadata["EMAIL_SECRET_KEY"],
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


def init_config() -> None:
    config_manager = ConfigManager()
    config_manager.init()
