import uuid

import pytest

from lifehub.clients.db.user import UserTokenRepository
from lifehub.models.user_old import UserToken


@pytest.fixture(scope="module")
def user_id():
    return uuid.uuid4()


@pytest.fixture(scope="function")
def db_client(engine, user_id):
    UserToken.metadata.create_all(bind=engine)
    yield UserTokenRepository(user_id)
    UserToken.metadata.drop_all(bind=engine)


def test_creation(db_client):
    """
    Test creating a UserTokenRepository object
    Expected: Object is created
    """
    assert db_client
