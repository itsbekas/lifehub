from typing import Any

from lifehub.config.constants import cfg
from lifehub.core.common.database_service import get_session
from lifehub.core.provider.repository.provider import ProviderRepository
from lifehub.core.provider.schema import (
    BasicProviderConfig,
    OAuthProviderConfig,
    Provider,
    ProviderConfig,
    TokenProviderConfig,
)
from lifehub.providers.gocardless.api_client import GoCardlessAPIClient
from lifehub.providers.google_calendar.api_client import GoogleCalendarAPIClient
from lifehub.providers.google_tasks.api_client import GoogleTasksAPIClient
from lifehub.providers.spotify.api_client import SpotifyAPIClient
from lifehub.providers.strava.api_client import StravaAPIClient
from lifehub.providers.trading212.api_client import Trading212APIClient
from lifehub.providers.ynab.api_client import YNABAPIClient

PROVIDER_CLIENTS = {
    "gocardless": GoCardlessAPIClient,
    "google_calendar": GoogleCalendarAPIClient,
    "google_tasks": GoogleTasksAPIClient,
    "spotify": SpotifyAPIClient,
    "strava": StravaAPIClient,
    "trading212": Trading212APIClient,
    "ynab": YNABAPIClient,
}


def init_setup_data() -> dict[str, dict[str, Any]]:
    provider_configs: dict[str, dict[str, Any]] = {
        "gocardless": {
            "name": "GoCardless",
            "auth_type": "token",
        },
        "google_calendar": {
            "name": "Google Calendar",
            "auth_type": "oauth",
            "auth_url": "https://accounts.google.com/o/oauth2/auth",
            "token_url": "https://accounts.google.com/o/oauth2/token",
            "client_id": cfg.GOOGLE_CALENDAR_CLIENT_ID,
            "client_secret": cfg.GOOGLE_CALENDAR_CLIENT_SECRET,
            "scope": "https://www.googleapis.com/auth/calendar.readonly",
        },
        "google_tasks": {
            "name": "Google Tasks",
            "auth_type": "oauth",
            "auth_url": "https://accounts.google.com/o/oauth2/auth",
            "token_url": "https://accounts.google.com/o/oauth2/token",
            "client_id": cfg.GOOGLE_TASKS_CLIENT_ID,
            "client_secret": cfg.GOOGLE_TASKS_CLIENT_SECRET,
            "scope": "https://www.googleapis.com/auth/tasks",
        },
        "spotify": {
            "name": "Spotify",
            "auth_type": "oauth",
            "auth_url": "https://accounts.spotify.com/authorize",
            "token_url": "https://accounts.spotify.com/api/token",
            "client_id": cfg.SPOTIFY_CLIENT_ID,
            "client_secret": cfg.SPOTIFY_CLIENT_SECRET,
            "scope": "user-read-private user-read-email",
        },
        "strava": {
            "name": "Strava",
            "auth_type": "oauth",
            "auth_url": "https://www.strava.com/oauth/authorize",
            "token_url": "https://www.strava.com/oauth/token",
            "client_id": cfg.STRAVA_CLIENT_ID,
            "client_secret": cfg.STRAVA_CLIENT_SECRET,
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
            "client_id": cfg.YNAB_CLIENT_ID,
            "client_secret": cfg.YNAB_CLIENT_SECRET,
            "scope": "read-only",
        },
    }

    return provider_configs


def setup_providers() -> None:
    provider_configs = init_setup_data()

    session = get_session()
    providers_dict = {}

    provider_repo = ProviderRepository(session)

    for provider_id in provider_configs:
        if provider_repo.get_by_id(provider_id) is not None:
            continue

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
    session.close()
