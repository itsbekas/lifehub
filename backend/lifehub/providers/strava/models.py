from __future__ import annotations

import datetime as dt
from typing import Any


class DetailedAthlete:
    def __init__(
        self,
        id: int,
        username: str,
        resource_state: int,
        firstname: str,
        lastname: str,
        bio: str,
        profile_medium: str,
        profile: str,
        city: str,
        state: str,
        country: str,
        sex: str,
        premium: bool, # Deprecated, use `summit` instead
        summit: bool,
        created_at: str,
        updated_at: str,
        badge_type_id: int,
        friend: str | None,
        follower: str | None,
        weight: float | None,
        measurement_preference: str | None = None,
        follower_count: int | None = None,
        friend_count: int | None = None,
        ftp: int | None = None,
        clubs: list[dict[str, Any]] | None = None,
        bikes: list[dict[str, Any]] | None = None,
        shoes: list[dict[str, Any]] | None = None,
    ):
        self.id: int = id
        self.username: str = username
        self.resource_state: int = resource_state
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.bio: str = bio
        self.profile_medium: str = profile_medium
        self.profile: str = profile
        self.city: str = city
        self.state: str = state
        self.country: str = country
        self.sex: str = sex
        self.premium: bool = premium
        self.summit: bool = summit
        self.created_at: dt.datetime = dt.datetime.fromisoformat(created_at)
        self.updated_at: dt.datetime = dt.datetime.fromisoformat(updated_at)
        self.badge_type_id: int = badge_type_id
        self.friend: str | None = friend
        self.follower: str | None = follower
        self.follower_count: int | None = follower_count
        self.friend_count: int | None = friend_count
        self.measurement_preference: str | None = measurement_preference
        self.ftp: int | None = ftp
        self.weight: float | None = weight
        self.clubs: list[dict[str, Any]] | None = clubs
        self.bikes: list[dict[str, Any]] | None = bikes
        self.shoes: list[dict[str, Any]] | None = shoes

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> DetailedAthlete:
        return cls(**data)

    def __repr__(self) -> str:
        return f"<Strava DetailedAthlete: {self.firstname} {self.lastname}>"
