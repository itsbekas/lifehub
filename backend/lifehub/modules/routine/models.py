from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class TaskResponse:
    id: str
    title: str
    due: Optional[str]


@dataclass
class TaskListResponse:
    id: str
    title: str
    tasks: list[TaskResponse]
