from sqlmodel import Session

from .client import DatabaseClient

__db_client = DatabaseClient.get_instance()


def get_session() -> Session:
    return Session(__db_client.engine)