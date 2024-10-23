import datetime as dt

import pytest
from sqlmodel import Field, SQLModel

from lifehub.clients.db.db import TimeBaseRepository


# Test model
class TimeBaseTestModel(SQLModel, table=True):
    date: dt.datetime = Field(primary_key=True)
    text: str = Field(max_length=16)


@pytest.fixture(scope="module")
def date_oldest():
    return dt.datetime(2023, 3, 3)


@pytest.fixture(scope="module")
def date_latest():
    return dt.datetime(2024, 4, 4)


@pytest.fixture(scope="function")
def db_client(engine):
    TimeBaseTestModel.metadata.create_all(bind=engine)
    yield TimeBaseRepository(TimeBaseTestModel)
    TimeBaseTestModel.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def obj_oldest(date_oldest):
    return TimeBaseTestModel(date=date_oldest, text="obj_oldest")


@pytest.fixture(scope="function")
def obj_latest(date_latest):
    return TimeBaseTestModel(date=date_latest, text="obj_latest")


def test_creation(db_client):
    """
    Test creating a TimeBaseRepository object
    Expected: Object is created
    """
    assert db_client


class TestGetLatest:
    def test_single(self, db_client, obj_latest):
        """
        Test getting the latest object from the database
        Expected: The object is returned
        """
        db_client.add(obj_latest)
        assert db_client.get_latest() == obj_latest

    def test_multiple(self, db_client, obj_oldest, obj_latest):
        """
        Test getting the latest object from the database with multiple objects
        Expected: The latest object is returned
        """
        db_client.add(obj_oldest)
        db_client.add(obj_latest)
        assert db_client.get_latest() == obj_latest

    def test_empty(self, db_client):
        """
        Test getting the latest object from an empty database
        Expected: None is returned
        """
        assert db_client.get_latest() is None
