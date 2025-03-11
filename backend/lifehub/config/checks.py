import datetime as dt
import time

from lifehub.config.constants import cfg
from lifehub.config.providers import setup_providers
from lifehub.config.util.schemas import *  # noqa: F401,F403
from lifehub.config.vault import setup_vault
from lifehub.core.common.base.db_model import BaseModel
from lifehub.core.common.database_service import get_engine, get_session
from lifehub.core.provider.repository.provider import ProviderRepository
from lifehub.core.user.service.user import UserService, UserServiceException
from lifehub.providers.gocardless.api_client import GoCardlessAPIClient


def check_mariadb() -> None:
    timeout: int = 60
    interval: int = 5
    start_time = time.time()
    engine = get_engine()
    while True:
        try:
            connection = engine.connect()
            connection.close()
            print("Successfully connected to MariaDB")
            break
        except Exception as e:
            if time.time() - start_time > timeout:
                print("Could not connect to MariaDB within the timeout period")
                exit(1)
            print("MariaDB not ready, waiting...")
            print(e)
            time.sleep(interval)


def setup_admin_user() -> None:
    with get_session() as session:
        user_service = UserService(session)

        try:
            user = user_service.create_user(
                cfg.ADMIN_USERNAME,
                "admin@life.hub",
                cfg.ADMIN_PASSWORD,
                "Admin",
            )
            user.verified = True
        except UserServiceException as e:
            if e.status_code != 409:
                raise
            user = user_service.get_user(cfg.ADMIN_USERNAME)
            user_service.update_user(
                user,
                "Admin",
                "admin@lifehub",
                cfg.ADMIN_PASSWORD,
            )
        session.commit()


def setup_admin_tokens() -> None:
    with get_session() as session:
        user_service = UserService(session)
        provider_repo = ProviderRepository(session)

        admin = user_service.get_user(cfg.ADMIN_USERNAME)

        gocardless_provider = provider_repo.get_by_id("gocardless")
        if gocardless_provider is None:
            raise Exception("Provider GoCardless not found in the database")

        # If the admin user has no token, add an empty one to be updated
        try:
            user_service.add_provider_token_to_user(
                admin,
                gocardless_provider,
                "",
                None,
                dt.datetime.now(),
                dt.datetime.max,
                skip_test=True,
            )
        except UserServiceException as e:
            if e.status_code != 409:
                raise

        gocardless_token = GoCardlessAPIClient(admin, session).get_token()

        user_service.update_provider_token(
            admin,
            gocardless_provider,
            gocardless_token.access,
            gocardless_token.refresh,
            dt.datetime.now() + dt.timedelta(seconds=gocardless_token.access_expires),
        )

        session.commit()


# Deprecated. Likely to be replaced with pre_run_setup()
# Or maybe just make the fetchers depend on the api through docker compose
def pre_run_checks() -> None:
    check_mariadb()


def create_db_tables() -> None:
    BaseModel.metadata.create_all(get_engine(admin=True))


def pre_run_setup() -> None:
    cfg._load_env()
    setup_vault()  # Must run before db checks since it sets up the db credentials
    cfg._load_vault_secrets()
    check_mariadb()
    create_db_tables()
    setup_providers()
    setup_admin_user()
    setup_admin_tokens()
