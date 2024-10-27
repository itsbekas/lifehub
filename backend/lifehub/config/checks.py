import time

from sqlalchemy import create_engine

from lifehub.config.constants import ADMIN_PASSWORD, ADMIN_USERNAME, DATABASE_URL
from lifehub.config.providers import setup_providers
from lifehub.config.util.schemas import *  # noqa: F401,F403
from lifehub.core.common.base.db_model import BaseModel
from lifehub.core.common.database_service import Session, engine
from lifehub.core.user.schema import User


def check_mariadb() -> None:
    timeout: int = 60
    interval: int = 5
    start_time = time.time()
    while True:
        try:
            connection = engine.connect()
            connection.close()
            print("Successfully connected to MariaDB")
            break
        except Exception:
            if time.time() - start_time > timeout:
                print("Could not connect to MariaDB within the timeout period")
                exit(1)
            print("MariaDB not ready, waiting...")
            time.sleep(interval)


def setup_admin_user() -> None:
    user = User(
        username=ADMIN_USERNAME,
        email="admin@lifehub",
        password=ADMIN_PASSWORD,
        name="Admin",
        verified=True,
    )
    with Session() as session:
        # check if admin exists and update if necessary
        current_user = (
            session.query(User).filter(User.username == ADMIN_USERNAME).first()
        )
        if current_user:
            current_user.email = user.email
            current_user.password = user.password
            current_user.name = user.name
            current_user.verified = user.verified
        else:
            session.add(user)
        session.commit()


# Deprecated. Likely to be replaced with pre_run_setup()
# Or maybe just make the fetchers depend on the api through docker compose
def pre_run_checks() -> None:
    check_mariadb()


def create_db_tables() -> None:
    engine = create_engine(DATABASE_URL, echo=True)
    BaseModel.metadata.create_all(engine)


def pre_run_setup() -> None:
    check_mariadb()
    create_db_tables()
    setup_admin_user()
    setup_providers()
