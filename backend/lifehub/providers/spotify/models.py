from __future__ import annotations

from typing import Any


class User:
    def __init__(
        self,
        country: str,
        display_name: str,
        email: str,
        explicit_content: dict[str, bool],
        external_urls: dict[str, str],
        followers: dict[str, Any],
        href: str,
        id: str,
        images: list[dict[str, str]],
        product: str,
        type: str,
        uri: str,
    ):
        self.country = country
        self.display_name = display_name
        self.email = email
        self.explicit_content = explicit_content
        self.external_urls = external_urls
        self.followers = followers
        self.href = href
        self.id = id
        self.images = images
        self.product = product
        self.type = type
        self.uri = uri

    @classmethod
    def from_response(cls, res: dict[str, Any]) -> User:
        return cls(**res)

    def __repr__(self) -> str:
        return f"<Spotify User {self.display_name}>"
