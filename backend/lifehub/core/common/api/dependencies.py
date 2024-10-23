from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from lifehub.core.common.database_service import Session as DatabaseSession


def get_session() -> Session:
    return DatabaseSession()


SessionDep = Annotated[Session, Depends(get_session)]
