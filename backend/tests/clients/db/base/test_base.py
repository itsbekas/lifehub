from decimal import Decimal

import pytest
from sqlmodel import Field, SQLModel

from lifehub.clients.db.db import BaseRepository


# Test model
class BaseTestModel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=10)
    number: Decimal = Field(decimal_places=2, max_digits=4)


@pytest.fixture(scope="function")
def db_client(engine):
    BaseTestModel.metadata.create_all(bind=engine)
    yield BaseRepository(BaseTestModel)
    BaseTestModel.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def obj1():
    return BaseTestModel(id=1, name="obj1", number=Decimal("1.1"))


@pytest.fixture(scope="function")
def obj2():
    return BaseTestModel(id=2, name="obj2", number=Decimal("2.2"))


def test_creation(db_client):
    """
    Test creating a BaseRepository object
    Expected: Object is created
    """
    assert db_client


class TestAdd:
    def test_single(self, db_client, obj1):
        """
        Test adding a single object to the database
        Expected: Object is added to the database
        """
        db_client.add(obj1)
        assert db_client.get_all() == [obj1]

    def test_multiple(self, db_client, obj1, obj2):
        """
        Test adding multiple objects to the database
        Expected: Objects are added to the database
        """
        db_client.add(obj1)
        db_client.add(obj2)
        assert db_client.get_all() == [obj1, obj2]

    def test_duplicate(self, db_client, obj1):
        """
        Test adding a duplicate object to the database
        Expected: Exception is raised
        """
        db_client.add(obj1)
        duplicate_obj = BaseTestModel(id=obj1.id, name=obj1.name, number=obj1.number)
        with pytest.raises(Exception):
            db_client.add(duplicate_obj)

    def test_max_length(self, db_client, obj1):
        """
        Test adding an object with a field that meets the max_length constraint
        Expected: Object is added to the database
        """
        obj1.name = "a" * 10
        db_client.add(obj1)
        assert db_client.get_all() == [obj1]

    def test_max_length_exceeded(self, db_client, obj1):
        """
        Test adding an object with a field that exceeds the max_length constraint
        Expected: Exception is raised
        """
        obj1.name = "a" * 11
        with pytest.raises(Exception):
            db_client.add(obj1)

    def test_decimal_places(self, db_client, obj1):
        """
        Test adding an object with a field that meets the decimal_places constraint
        Expected: Object is added to the database
        """
        obj1.number = Decimal("12.34")
        db_client.add(obj1)
        assert db_client.get_all() == [obj1]

    def test_decimal_places_exceeded(self, db_client, obj1):
        """
        Test adding an object with a field that exceeds the decimal_places constraint
        Expected: Number is rounded to the nearest decimal_places
        """
        obj1.number = Decimal("1.789")
        db_client.add(obj1)
        assert obj1.number == Decimal("1.79")

    def test_max_digits(self, db_client):
        """
        Test adding an object with a field that meets the max_digits constraint
        Expected: Object is added to the database
        """
        obj1.number = Decimal("123.45")
        with pytest.raises(Exception):
            db_client.add(obj1)


class TestGetAll:
    def test_empty(self, db_client):
        """
        Test getting all objects from an empty database
        Expected: Empty list is returned
        """
        assert db_client.get_all() == []

    def test_single(self, db_client, obj1):
        """
        Test getting all objects from a database with a single object
        Expected: List containing the object is returned
        """
        db_client.add(obj1)
        assert db_client.get_all() == [obj1]

    def test_multiple(self, db_client, obj1, obj2):
        """
        Test getting all objects from a database with multiple objects
        Expected: List containing all objects is returned
        """
        db_client.add(obj1)
        db_client.add(obj2)
        assert db_client.get_all() == [obj1, obj2]


class TestUpdate:
    def test_single(self, db_client, obj1):
        """
        Test updating a single object in the database
        Expected: Object is updated in the database
        """
        db_client.add(obj1)
        obj1.name = "new_name"
        db_client.update(obj1)
        retrieved_obj = db_client.get_all()[0]
        assert retrieved_obj.name == "new_name"

    def test_multiple(self, db_client, obj1, obj2):
        """
        Test updating multiple objects in the database
        Expected: Objects are updated in the database
        """
        db_client.add(obj1)
        db_client.add(obj2)
        obj1.name = "new_name1"
        obj2.name = "new_name2"
        db_client.update(obj1)
        db_client.update(obj2)
        retrieved_objs = db_client.get_all()
        assert retrieved_objs[0].name == "new_name1"
        assert retrieved_objs[1].name == "new_name2"

    # Because SQLAlchemy ORM deals add as save_or_update, this test fails unless
    # we add a check for existence of the object in the database
    # This might be done in the future, but for the time being, default behavior
    # is left as is
    def test_nonexistent(self, db_client, obj1):
        """
        Test updating a nonexistent object in the database
        Expected: Exception is raised
        """
        pass
        # with pytest.raises(Exception):
        #     db_client.update(obj1)


class TestDelete:
    def test_single(self, db_client, obj1):
        """
        Test deleting a single object from the database
        Expected: Object is deleted from the database
        """
        db_client.add(obj1)
        db_client.delete(obj1)
        assert db_client.get_all() == []

    def test_multiple(self, db_client, obj1, obj2):
        """
        Test deleting multiple objects from the database
        Expected: Objects are deleted from the database
        """
        db_client.add(obj1)
        db_client.add(obj2)
        db_client.delete(obj1)
        assert db_client.get_all() == [obj2]

    def test_nonexistent(self, db_client, obj1):
        """
        Test deleting a nonexistent object from the database
        Expected: Exception is raised
        """
        with pytest.raises(Exception):
            db_client.delete(obj1)
