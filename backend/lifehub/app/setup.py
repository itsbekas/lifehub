from sqlalchemy import create_engine

from lifehub.config.checks import pre_run_checks
from lifehub.config.constants import DATABASE_URL
from lifehub.config.providers import setup_providers
from lifehub.config.util.schemas import *  # noqa: F401,F403
from lifehub.core.common.base.db_model import BaseModel


def setup() -> None:
    pre_run_checks()

    engine = create_engine(DATABASE_URL, echo=True)

    BaseModel.metadata.create_all(engine)

    setup_providers()


def clean() -> None:
    pre_run_checks()

    """
    Warning: This function will drop all tables and recreate them
    This is only for development purposes
    """
    input(
        "This will drop all tables in the database. Press Enter to continue or Ctrl+C to exit"
    )

    engine = create_engine(DATABASE_URL, echo=True)

    BaseModel.metadata.drop_all(engine)
