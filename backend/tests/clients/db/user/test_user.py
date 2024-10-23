import pytest

from lifehub.clients.db.user import UserRepository
from lifehub.models.user_old import User


@pytest.fixture(scope="function")
def db_client(engine):
    User.metadata.create_all(bind=engine)
    yield UserRepository()
    User.metadata.drop_all(bind=engine)


def test_creation(db_client):
    """
    Test creating a UserBaseRepository object
    Expected: Object is created
    """
    assert db_client
