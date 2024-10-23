from typing import Any

from lifehub.config.constants import getenv
from lifehub.core.common.database_service import Session
from lifehub.core.module.schema import Module
from lifehub.core.provider.schema import (
    BasicProviderConfig,
    OAuthProviderConfig,
    Provider,
    ProviderConfig,
    TokenProviderConfig,
)
from lifehub.providers.google_calendar.api_client import GoogleCalendarAPIClient
from lifehub.providers.spotify.api_client import SpotifyAPIClient
from lifehub.providers.strava.api_client import StravaAPIClient
from lifehub.providers.trading212.api_client import Trading212APIClient
from lifehub.providers.ynab.api_client import YNABAPIClient

PROVIDER_CLIENTS = {
    "google_calendar": GoogleCalendarAPIClient,
    "spotify": SpotifyAPIClient,
    "strava": StravaAPIClient,
    "trading212": Trading212APIClient,
    "ynab": YNABAPIClient,
}


def init_setup_data() -> tuple[dict[str, dict[str, Any]], dict[str, list[str]]]:
    provider_configs: dict[str, dict[str, Any]] = {
        "google_calendar": {
            "name": "Google Calendar",
            "auth_type": "oauth",
            "auth_url": "https://accounts.google.com/o/oauth2/auth",
            "token_url": "https://accounts.google.com/o/oauth2/token",
            "client_id": getenv("GOOGLE_CALENDAR_CLIENT_ID"),
            "client_secret": getenv("GOOGLE_CALENDAR_CLIENT_SECRET"),
            "scope": "https://www.googleapis.com/auth/calendar.readonly",
        },
        "spotify": {
            "name": "Spotify",
            "auth_type": "oauth",
            "auth_url": "https://accounts.spotify.com/authorize",
            "token_url": "https://accounts.spotify.com/api/token",
            "client_id": getenv("SPOTIFY_CLIENT_ID"),
            "client_secret": getenv("SPOTIFY_CLIENT_SECRET"),
            "scope": "user-read-private user-read-email",
        },
        "strava": {
            "name": "Strava",
            "auth_type": "oauth",
            "auth_url": "https://www.strava.com/oauth/authorize",
            "token_url": "https://www.strava.com/oauth/token",
            "client_id": getenv("STRAVA_CLIENT_ID"),
            "client_secret": getenv("STRAVA_CLIENT_SECRET"),
            "scope": "activity:read_all",
        },
        "trading212": {
            "name": "Trading212",
            "auth_type": "token",
        },
        "ynab": {
            "name": "YNAB",
            "auth_type": "oauth",
            "auth_url": "https://app.ynab.com/oauth/authorize",
            "token_url": "https://app.ynab.com/oauth/token",
            "client_id": getenv("YNAB_CLIENT_ID"),
            "client_secret": getenv("YNAB_CLIENT_SECRET"),
            "scope": "read-only",
        },
    }

    module_providers: dict[str, list[str]] = {
        "networth": ["trading212", "ynab"],
        "t212history": ["trading212"],
    }

    return provider_configs, module_providers


def setup_providers() -> None:
    provider_configs, module_providers = init_setup_data()

    session = Session()
    providers_dict = {}

    for provider_id in provider_configs:
        config = provider_configs[provider_id]
        provider = Provider(id=provider_id, name=config["name"])
        session.add(provider)
        providers_dict[provider_id] = provider

        provider_config: ProviderConfig

        if config["auth_type"] == "oauth":
            provider_config = OAuthProviderConfig(
                provider_id=provider.id,
                auth_url=config["auth_url"],
                allow_custom_url=config.get("allow_custom_url", False),
                token_url=config["token_url"],
                client_id=config["client_id"],
                client_secret=config["client_secret"],
                scope=config["scope"],
            )
        elif config["auth_type"] == "token":
            provider_config = TokenProviderConfig(
                provider_id=provider.id,
                allow_custom_url=config.get("allow_custom_url", False),
            )
        elif config["auth_type"] == "basic":
            provider_config = BasicProviderConfig(
                provider_id=provider.id,
                allow_custom_url=config.get("allow_custom_url", False),
            )

        provider.config = provider_config
        session.add(provider_config)

    session.commit()

    modules = []
    for module_name, provider_names in module_providers.items():
        module_providers_list = [
            providers_dict[provider_name] for provider_name in provider_names
        ]
        module = Module(name=module_name, providers=module_providers_list)
        modules.append(module)
        session.add(module)

    session.commit()

    session.close()
