from lifehub.config.checks import pre_run_checks
from lifehub.config.providers import setup_providers
from lifehub.config.util.schemas import *  # noqa: F401,F403
from lifehub.core.common.base.db_model import BaseModel
from lifehub.core.common.database_service import get_engine


def setup() -> None:
    pre_run_checks()

    BaseModel.metadata.create_all(get_engine())

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

    BaseModel.metadata.drop_all(get_engine())
