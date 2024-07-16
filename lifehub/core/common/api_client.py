import datetime as dt
from abc import ABC, abstractmethod
from os import getenv
from typing import Any, Callable, Optional

import requests
from sqlalchemy.orm import Session as SessionType

from lifehub.core.provider.repository.provider import ProviderRepository
from lifehub.core.provider.repository.provider_token import ProviderTokenRepository
from lifehub.core.provider.schema import Provider, ProviderToken, is_oauth_config
from lifehub.core.user.schema import User


def request_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(self: "APIClient", endpoint: str, *args: Any, **kwargs: Any) -> Any:
        try:
            url = f"{self.base_url}/{endpoint}"
            res = func(self, url, *args, **kwargs)
            if res.status_code != 200:
                raise APIException(
                    type(self).__name__, url, res.status_code, self._error_msg(res)
                )
            return res.json()
        except requests.exceptions.RequestException as e:
            raise APIException(
                type(self).__name__,
                url,
                500,
                f"Error accessing {self.base_url}: {str(e)}",
            )

    return wrapper


class APIException(Exception):
    def __init__(self, api: str, url: str, status_code: int, msg: str) -> None:
        self.api = api
        self.url = url
        self.status_code = status_code
        self.msg = msg

    def __str__(self) -> str:
        return f"{self.api} API: Error accessing {self.url} - HTTP {self.status_code}: {self.msg}"


class APIClient(ABC):
    provider_name: str
    base_url: str
    headers: Optional[dict[str, str]]
    cookies: Optional[dict[str, str]]

    def __init__(self, user: User, session: SessionType) -> None:
        self.user = user

        provider: Provider | None = ProviderRepository(session).get_by_name(
            self.provider_name
        )

        if provider is None:
            raise Exception(f"Provider {self.provider_name} not found in the database")

        self.provider: Provider = provider

        tokenRepo: ProviderTokenRepository = ProviderTokenRepository(session)

        token: ProviderToken | None = tokenRepo.get(user, self.provider)

        if token is None:
            raise Exception(f"Token not found for {self.provider_name} provider")

        self.token: ProviderToken = token
        session.merge(self.token)

        if self.token.expires_at < dt.datetime.now():
            self._refresh_token(tokenRepo)
            session.commit()

    @property
    def _token_headers(self) -> dict[str, str]:
        return {"Authorization": self.token.token}

    @property
    def _token_bearer_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token.token}"}

    def _refresh_token(self, tokenRepo: ProviderTokenRepository) -> None:
        config = self.provider.config
        if not is_oauth_config(config):
            raise Exception("Attempting to refresh token for non-OAuth provider")
        url = config.build_refresh_token_url(self.token.refresh_token)
        res = requests.post(url)
        if res.status_code != 200:
            raise APIException(
                type(self).__name__, url, res.status_code, "Error refreshing token"
            )
        data = res.json()

        self.token.token = data["access_token"]
        self.token.expires_at = dt.datetime.now() + dt.timedelta(
            seconds=data["expires_in"]
        )
        tokenRepo.update(self.token)

    @abstractmethod
    def _get(self, endpoint: str, params: dict[str, Any] = {}) -> Any:
        """
        GET request to the API
        """
        pass

    @abstractmethod
    def _post(self, endpoint: str, data: dict[str, Any] = {}) -> Any:
        """
        POST request to the API
        """
        pass

    @request_handler
    def _get_basic(self, url: str, params: dict[str, Any]) -> Any:
        """
        Basic GET request to the API
        """
        return requests.get(url, params=params)

    @request_handler
    def _get_with_headers(self, url: str, params: dict[str, Any]) -> Any:
        """
        GET request to the API with custom headers
        """
        return requests.get(url, headers=self.headers, params=params)

    @request_handler
    def _get_with_cookies(self, url: str, params: dict[str, Any]) -> Any:
        """
        GET request to the API with cookies
        """
        return requests.get(url, cookies=self.cookies, params=params)

    @request_handler
    def _post_basic(self, url: str, data: dict[str, Any]) -> Any:
        """
        Basic POST request to the API
        """
        return requests.post(url, data=data)

    @request_handler
    def _post_with_headers(self, url: str, data: dict[str, Any]) -> Any:
        """
        POST request to the API with custom headers
        """
        return requests.post(url, headers=self.headers, data=data)

    @request_handler
    def _post_with_cookies(self, url: str, data: dict[str, Any]) -> Any:
        """
        POST request to the API with cookies
        """
        return requests.post(url, cookies=self.cookies, data=data)

    @abstractmethod
    def _error_msg(self, res: requests.Response) -> str:
        """
        Get the error message from the response
        """
        pass

    def _load_env_token(self, env_var: str) -> str | None:
        """
        Load token from environment variable
        """

        return getenv(env_var)

    @abstractmethod
    def _test(self) -> None:
        """
        Test connection to the API
        Should be a self._get() or self._post() request to a basic endpoint
        """
        pass

    def test_connection(self) -> bool:
        """
        Test connection to the API
        """
        try:
            self._test()
            return True
        except APIException:
            return False
