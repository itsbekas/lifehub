from __future__ import annotations

import datetime as dt
import time
from abc import ABC, abstractmethod
from dataclasses import asdict, is_dataclass
from enum import Enum
from functools import wraps
from os import getenv
from typing import TYPE_CHECKING, Any, Callable, Optional, TypeIs, TypeVar, cast

import requests
from sqlalchemy.orm import Session as SessionType

from lifehub.core.provider.repository.provider import ProviderRepository
from lifehub.core.provider.repository.provider_token import ProviderTokenRepository
from lifehub.core.provider.schema import Provider, ProviderToken, is_oauth_config
from lifehub.core.user.repository.user import UserRepository
from lifehub.core.user.schema import User

if TYPE_CHECKING:
    from _typeshed import DataclassInstance

    RequestParams = DataclassInstance

T = TypeVar("T", bound=Callable[..., Any])


class AuthType(Enum):
    BASIC = "basic"
    HEADERS = "headers"
    TOKEN_HEADERS = "token_headers"
    TOKEN_BEARER_HEADERS = "token_bearer_headers"
    OAUTH = TOKEN_BEARER_HEADERS
    COOKIES = "cookies"


def auth_override(auth_type: AuthType) -> Callable[[T], T]:
    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(self: APIClient, *args: Any, **kwargs: Any) -> Any:
            original_auth_type = self.auth_type
            try:
                self.auth_type = auth_type
                return func(self, *args, **kwargs)
            finally:
                self.auth_type = original_auth_type

        return cast(T, wrapper)

    return decorator


def request_handler(func: T) -> T:
    """
    A wrapper for request functions
    Handles retries and rate limiting (with exponential backoff if a Retry-After header isn't provided)
    Raises an APIException if the status code is not 200
    """

    @wraps(func)
    def wrapper(self: "APIClient", endpoint: str, *args: Any, **kwargs: Any) -> Any:
        url = f"{self.base_url}/{endpoint}"
        max_retries = 5
        backoff_factor = 2
        delay = 1

        def is_dataclass_obj(obj: Any) -> TypeIs[RequestParams]:
            return is_dataclass(obj) and not isinstance(obj, type)

        def prepare_kwargs(kwargs: dict[str, Any]) -> dict[str, Any]:
            if "params" in kwargs and is_dataclass_obj(kwargs["params"]):
                kwargs["params"] = asdict(kwargs["params"])
            if "data" in kwargs and is_dataclass_obj(kwargs["data"]):
                kwargs["data"] = asdict(kwargs["data"])
            return kwargs

        def exponential_backoff(retry_count: int, retry_after: Optional[int]) -> None:
            wait_time = (
                retry_after
                if retry_after is not None
                else delay * (backoff_factor**retry_count)
            )
            time.sleep(wait_time)

        kwargs = prepare_kwargs(kwargs)

        for attempt in range(max_retries):
            try:
                res = func(self, url, *args, **kwargs)
                if res.status_code == 429:
                    retry_after = int(res.headers.get("Retry-After", delay))
                    exponential_backoff(attempt, retry_after)
                    continue
                if not (200 <= res.status_code < 300):
                    raise APIException(
                        type(self).__name__, url, res.status_code, self._error_msg(res)
                    )
                return res.json()
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise APIException(
                        type(self).__name__,
                        url,
                        500,
                        f"Error accessing {self.base_url}: {str(e)}",
                    )

    return cast(T, wrapper)


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

    @property
    @abstractmethod
    def auth_type(self) -> AuthType:
        pass

    @auth_type.setter
    def auth_type(self, value: AuthType) -> None:
        self.auth_type = value

    def __init__(
        self, user: User, session: SessionType, token_username: str = ""
    ) -> None:
        # token_user allows overriding the user for the token
        # This is useful for providers such as GoCardless where the admin token is used
        # and client tokens are passed in the request body
        if token_username:
            token_user = UserRepository(session).get_by_username(token_username)

            if token_user is None:
                raise Exception(f"User {token_username} not found in the database")
        else:
            token_user = user

        self.user = user

        provider: Provider | None = ProviderRepository(session).get_by_id(
            self.provider_name
        )

        if provider is None:
            raise Exception(f"Provider {self.provider_name} not found in the database")

        self.provider: Provider = provider

        tokenRepo: ProviderTokenRepository = ProviderTokenRepository(session)

        token: ProviderToken | None = tokenRepo.get(token_user, self.provider)

        if token is None:
            raise Exception(f"Token not found for {self.provider_name} provider")

        self.token: ProviderToken = token
        session.merge(self.token)

        if self.token.expires_at < dt.datetime.now():
            self._refresh_token(tokenRepo)
            session.commit()

        match self.auth_type:
            case AuthType.BASIC:
                pass
            case AuthType.HEADERS:
                pass
            case AuthType.TOKEN_HEADERS:
                self.headers = {"Authorization": self.token.token}
            case AuthType.TOKEN_BEARER_HEADERS:
                self.headers = {"Authorization": f"Bearer {self.token.token}"}
            case AuthType.COOKIES:
                pass

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

    @request_handler
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[RequestParams] = None,
        data: Optional[RequestParams] = None,
        headers: Optional[dict[str, str]] = None,
        cookies: Optional[dict[str, str]] = None,
    ) -> Any:
        """
        Generalized request handler to perform HTTP requests with various configurations.
        """

        if headers is not None and self.headers is not None:
            headers = {**self.headers, **headers}

        url = f"{self.base_url}/{endpoint}"
        request_method = getattr(requests, method.lower())
        return request_method(
            url, params=params, data=data, headers=headers, cookies=cookies
        )

    def _get(self, endpoint: str, params: Optional[RequestParams] = None) -> Any:
        return self._request("GET", endpoint, params=params)

    def _post(
        self,
        endpoint: str,
        params: Optional[RequestParams] = None,
        data: Optional[RequestParams] = None,
    ) -> Any:
        return self._request("POST", endpoint, params=params, data=data)

    def _put(
        self,
        endpoint: str,
        params: Optional[RequestParams] = None,
        data: Optional[RequestParams] = None,
    ) -> Any:
        return self._request("PUT", endpoint, params=params, data=data)

    def _delete(self, endpoint: str, params: Optional[RequestParams] = None) -> Any:
        return self._request("DELETE", endpoint, params=params)

    def _patch(
        self,
        endpoint: str,
        params: Optional[RequestParams] = None,
        data: Optional[RequestParams] = None,
    ) -> Any:
        return self._request("PATCH", endpoint, params=params, data=data)

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
