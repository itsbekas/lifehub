from typing import Generic, Sequence, Type

from sqlalchemy import select
from sqlalchemy.orm import Session

from lifehub.core.common.repository import BaseModelType


class BaseRepository(Generic[BaseModelType]):
    def __init__(self, model: Type[BaseModelType], session: Session) -> None:
        self.model: Type[BaseModelType] = model
        self.session = session

    def add(self, obj: BaseModelType) -> None:
        self.session.add(obj)

    def get_all(self) -> Sequence[BaseModelType]:
        statement = select(self.model)
        result = self.session.execute(statement)
        return result.scalars().all()

    def update(self, obj: BaseModelType) -> None:
        self.session.add(obj)

    def delete(self, obj: BaseModelType) -> None:
        self.session.delete(obj)

    def merge(self, obj: BaseModelType) -> BaseModelType:
        return self.session.merge(obj)

    def commit(self) -> None:
        self.session.commit()

    def refresh(self, obj: BaseModelType) -> None:
        self.session.refresh(obj)

    def rollback(self) -> None:
        self.session.rollback()

    def close(self) -> None:
        self.session.close()
