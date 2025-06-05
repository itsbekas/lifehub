from typing import TypeVar

from lifehub.core.common.base.db_model import BaseModel, TimeBaseModel, UserBaseModel

BaseModelType = TypeVar("BaseModelType", bound=BaseModel)
UserBaseModelType = TypeVar("UserBaseModelType", bound=UserBaseModel)
TimeBaseModelType = TypeVar("TimeBaseModelType", bound=TimeBaseModel)
