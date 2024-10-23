import datetime as dt
import uuid

import pytest
from sqlmodel import Field, SQLModel

from lifehub.clients.db.db import TimeUserBaseRepository


# Test model
class TimeUserBaseTestModel(SQLModel, table=True):
    user_id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    timestamp: dt.datetime = Field(primary_key=True, default_factory=dt.datetime.now)
    text: str = Field(max_length=16)


@pytest.fixture(scope="module")
def date_oldest():
    return dt.datetime(2023, 3, 3)


@pytest.fixture(scope="module")
def date_latest():
    return dt.datetime(2024, 4, 4)


@pytest.fixture(scope="module")
def user_id1():
    return uuid.uuid4()


@pytest.fixture(scope="module")
def user_id2():
    return uuid.uuid4()


@pytest.fixture(scope="function")
def db_client(engine, user_id1):
    TimeUserBaseTestModel.metadata.create_all(bind=engine)
    yield TimeUserBaseRepository(TimeUserBaseTestModel, user_id1)
    TimeUserBaseTestModel.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def obj_oldest_user1(user_id1, date_oldest):
    return TimeUserBaseTestModel(
        user_id=user_id1, timestamp=date_oldest, text="obj_oldest1"
    )


@pytest.fixture(scope="function")
def obj_latest_user1(user_id1, date_latest):
    return TimeUserBaseTestModel(
        user_id=user_id1, timestamp=date_latest, text="obj_latest1"
    )


@pytest.fixture(scope="function")
def obj_oldest_user2(user_id2, date_oldest):
    return TimeUserBaseTestModel(
        user_id=user_id2, timestamp=date_oldest, text="obj_oldest2"
    )


@pytest.fixture(scope="function")
def obj_latest_user2(user_id2, date_latest):
    return TimeUserBaseTestModel(
        user_id=user_id2, timestamp=date_latest, text="obj_latest2"
    )


def test_creation(db_client):
    """
    Test creating a TimeUserBaseRepository object
    Expected: Object is created
    """
    assert db_client


class TestGetLatest:
    def test_empty(self, db_client):
        """
        Test getting the latest object from an empty database
        Expected: None is returned
        """
        assert db_client.get_latest() is None

    def test_single_correct_user(self, db_client, obj_latest_user1):
        """
        Test getting the latest object from the database with a single object
        Expected: The object is returned
        """
        db_client.add(obj_latest_user1)
        assert db_client.get_latest() == obj_latest_user1

    def test_single_incorrect_user(self, db_client, obj_latest_user2):
        """
        Test getting the latest object from the database with a single object
        Expected: None is returned
        """
        user2_db_client = TimeUserBaseRepository(
            TimeUserBaseTestModel, obj_latest_user2.user_id
        )
        user2_db_client.add(obj_latest_user2)
        assert db_client.get_latest() is None

    def test_multiple_correct_user(self, db_client, obj_oldest_user1, obj_latest_user1):
        """
        Test getting the latest object from the database with multiple objects
        Expected: The latest object is returned
        """
        db_client.add(obj_oldest_user1)
        db_client.add(obj_latest_user1)
        assert db_client.get_latest() == obj_latest_user1

    def test_multiple_incorrect_user(
        self, db_client, obj_oldest_user1, obj_latest_user2
    ):
        """
        Test getting the latest object from a database where the latest object has the incorrect user ID
        Expected: Correct user's latest object is returned
        """
        db_client.add(obj_oldest_user1)
        user2_db_client = TimeUserBaseRepository(
            TimeUserBaseTestModel, obj_latest_user2.user_id
        )
        user2_db_client.add(obj_latest_user2)
        assert db_client.get_latest() == obj_oldest_user1
