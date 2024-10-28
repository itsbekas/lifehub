from pydantic.dataclasses import dataclass


@dataclass
class TaskListResponse:
    kind: str
    id: str
    etag: str
    title: str
    updated: str
    selfLink: str
