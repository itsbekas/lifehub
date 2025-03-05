from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from lifehub.core.common.database_service import get_session

SessionDep = Annotated[Session, Depends(get_session)]
