import uuid

import pytest

from lifehub.clients.db.finance import T212TransactionDBClient
from lifehub.modules.finance.models import T212Transaction


@pytest.fixture(scope="module")
def user_id():
    return uuid.uuid4()


@pytest.fixture(scope="function")
def db_client(engine, user_id):
    T212Transaction.metadata.create_all(bind=engine)
    yield T212TransactionDBClient(user_id)
    T212Transaction.metadata.drop_all(bind=engine)


def test_creation(db_client):
    """
    Test creating a T212TransactionDBClient object
    Expected: Object is created
    """
    assert db_client
