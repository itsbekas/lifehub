from typing import TypeVar

from lifehub.core.common.base_model import (
    BaseModel,
    FetchBaseModel,
    TimeBaseModel,
    UserBaseModel,
)

BaseModelType = TypeVar("BaseModelType", bound=BaseModel)
UserBaseModelType = TypeVar("UserBaseModelType", bound=UserBaseModel)
TimeBaseModelType = TypeVar("TimeBaseModelType", bound=TimeBaseModel)
FetchBaseModelType = TypeVar("FetchBaseModelType", bound=FetchBaseModel)
