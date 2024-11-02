from dataclasses import field
from typing import Any, Dict, List, Optional, Union

from pydantic.dataclasses import dataclass


@dataclass
class TaskListResponse:
    kind: str
    id: str
    etag: str
    title: str
    updated: str
    selfLink: str


@dataclass
class TaskLink:
    type: str
    description: str
    link: str


@dataclass
class ListTasklistsRequest:
    maxResults: Optional[int] = 20
    pageToken: Optional[str] = None


@dataclass
class ListTasksRequest:
    completedMax: Optional[str] = None
    completedMin: Optional[str] = None
    dueMax: Optional[str] = None
    dueMin: Optional[str] = None
    maxResults: Optional[int] = 20
    pageToken: Optional[str] = None
    showCompleted: Optional[bool] = True
    showDeleted: Optional[bool] = False
    showHidden: Optional[bool] = False
    updatedMin: Optional[str] = None
    showAssigned: Optional[bool] = False


@dataclass
class TaskResponse:
    kind: str
    id: str
    etag: str
    title: str
    updated: str
    selfLink: str
    status: str
    deleted: bool = False
    hidden: bool = False
    parent: Optional[str] = None
    position: Optional[str] = None
    notes: Optional[str] = None
    due: Optional[str] = None
    completed: Optional[str] = None
    links: List[TaskLink] = field(default_factory=list)
    webViewLink: Optional[str] = None
    assignmentInfo: Optional[Dict[str, Any]] = None


@dataclass
class TaskCompleteRequest:
    status: str = "completed"


TaskUpdateRequest = Union[TaskCompleteRequest]
