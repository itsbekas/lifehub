from __future__ import annotations

from typing import TYPE_CHECKING

import hvac
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lifehub.config.constants import (
    DB_HOST,
    DB_NAME,
    VAULT_ADDR,
    VAULT_DB_ADMIN_ROLE,
    VAULT_DB_ROLE,
    VAULT_TOKEN,
)

if TYPE_CHECKING:
    from sqlalchemy import Engine
    from sqlalchemy.orm import Session


def get_db_credentials(admin: bool = False) -> dict[str, str]:
    """
    Fetch dynamic credentials from Vault.
    """
    client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)
    role = VAULT_DB_ADMIN_ROLE if admin else VAULT_DB_ROLE
    creds = client.secrets.database.generate_credentials(name=role)

    return {
        "username": creds["data"]["username"],
        "password": creds["data"]["password"],
    }


def get_engine(admin: bool = False) -> Engine:
    """
    Create a SQLAlchemy engine with dynamic credentials.
    """
    creds = get_db_credentials(admin)
    db_url = f"mariadb+mariadbconnector://{creds['username']}:{creds['password']}@{DB_HOST}:3306/{DB_NAME}"
    return create_engine(db_url)


def get_session() -> Session:
    """
    Create a new database session dynamically.
    """
    engine = get_engine()
    return sessionmaker(bind=engine)()
