import uuid

import pytest

from lifehub.clients.db.finance import NetworthDBClient
from lifehub.modules.finance.schema import Networth


@pytest.fixture(scope="module")
def user_id():
    return uuid.uuid4()


@pytest.fixture(scope="function")
def db_client(engine, user_id):
    Networth.metadata.create_all(bind=engine)
    yield NetworthDBClient(user_id)
    Networth.metadata.drop_all(bind=engine)


def test_creation(db_client):
    """
    Test creating a NetworthDBClient object
    Expected: Object is created
    """
    assert db_client
