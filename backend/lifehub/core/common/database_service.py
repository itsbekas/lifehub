from __future__ import annotations

from typing import TYPE_CHECKING

import hvac
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lifehub.config.constants import cfg

if TYPE_CHECKING:
    from sqlalchemy import Engine
    from sqlalchemy.orm import Session


def get_db_credentials(admin: bool = False) -> dict[str, str]:
    """
    Fetch dynamic credentials from Vault.
    """
    client = hvac.Client(url=cfg.VAULT_ADDR, token=cfg.VAULT_TOKEN)
    role = cfg.VAULT_DB_ADMIN_ROLE if admin else cfg.VAULT_DB_ROLE
    creds = client.secrets.database.generate_credentials(
        name=role,
        mount_point=cfg.VAULT_DB_MOUNT_POINT,
    )

    return {
        "username": creds["data"]["username"],
        "password": creds["data"]["password"],
    }


def get_engine(admin: bool = False) -> Engine:
    """
    Create a SQLAlchemy engine with dynamic credentials.
    """
    creds = get_db_credentials(admin)
    db_url = f"mariadb+mariadbconnector://{creds['username']}:{creds['password']}@{cfg.DB_HOST}:3306/{cfg.DB_NAME}"
    return create_engine(db_url)


def get_session() -> Session:
    """
    Create a new database session dynamically.
    """
    engine = get_engine()
    return sessionmaker(bind=engine)()
