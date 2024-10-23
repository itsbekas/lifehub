import uuid

import pytest
from sqlmodel import Field, SQLModel

from lifehub.clients.db.db import UserBaseRepository


# Test model
class UserBaseTestModel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: uuid.UUID = Field()
    text: str = Field(max_length=10)


@pytest.fixture(scope="module")
def user_id1():
    return uuid.uuid4()


@pytest.fixture(scope="module")
def user_id2():
    return uuid.uuid4()


@pytest.fixture(scope="function")
def db_client(engine, user_id1):
    UserBaseTestModel.metadata.create_all(bind=engine)
    yield UserBaseRepository(UserBaseTestModel, user_id1)
    UserBaseTestModel.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def obj1_user1(user_id1):
    return UserBaseTestModel(id=1, user_id=user_id1, text="obj1")


@pytest.fixture(scope="function")
def obj2_user1(user_id1):
    return UserBaseTestModel(id=2, user_id=user_id1, text="obj2")


@pytest.fixture(scope="function")
def obj1_user2(user_id2):
    return UserBaseTestModel(id=1, user_id=user_id2, text="obj1")


@pytest.fixture(scope="function")
def obj2_user2(user_id2):
    return UserBaseTestModel(id=2, user_id=user_id2, text="obj2")


def test_creation(db_client):
    """
    Test creating a UserBaseRepository object
    Expected: Object is created
    """
    assert db_client


def test_creation_without_user_id():
    """
    Test creating a UserBaseRepository object without a user ID
    Expected: TypeError is raised
    """
    with pytest.raises(TypeError):
        UserBaseRepository(UserBaseTestModel)


class TestAdd:
    def test_correct_user(self, db_client, obj1_user1):
        """
        Test adding an object with the correct user ID
        Expected: Object is added to the database
        """
        db_client.add(obj1_user1)
        assert db_client.get_all() == [obj1_user1]

    def test_incorrect_user(self, db_client, obj1_user2):
        """
        Test adding an object with an incorrect user ID
        Expected: ValueError is raised
        """
        with pytest.raises(ValueError):
            db_client.add(obj1_user2)


class TestGetAll:
    def test_no_objects(self, db_client):
        """
        Test getting all objects when none are present
        Expected: No objects are returned
        """
        assert db_client.get_all() == []

    def test_correct_user(self, db_client, obj1_user1, obj2_user1):
        """
        Test getting all objects with the correct user ID
        Expected: All objects with the correct user ID are returned
        """
        db_client.add(obj1_user1)
        db_client.add(obj2_user1)
        assert db_client.get_all() == [obj1_user1, obj2_user1]

    def test_incorrect_user(self, db_client, user_id2, obj1_user2):
        """
        Test getting all objects when none have the correct user ID
        Expected: No objects are returned
        """
        user2_db_client = UserBaseRepository(UserBaseTestModel, user_id2)
        user2_db_client.add(obj1_user2)
        assert db_client.get_all() == []


class TestUpdate:
    def test_correct_user(self, db_client, obj1_user1, obj2_user1):
        """
        Test updating an object with the correct user ID
        Expected: Object is updated in the database
        """
        db_client.add(obj1_user1)
        db_client.add(obj2_user1)
        obj1_user1.text = "new_text"
        db_client.update(obj1_user1)
        assert db_client.get_all() == [obj1_user1, obj2_user1]

    def test_incorrect_user(self, db_client, obj1_user1, obj1_user2):
        """
        Test updating an object with an incorrect user ID
        Expected: ValueError is raised
        """
        db_client.add(obj1_user1)
        with pytest.raises(ValueError):
            db_client.update(obj1_user2)


class TestDelete:
    def test_correct_user(self, db_client, obj1_user1, obj2_user1):
        """
        Test deleting an object with the correct user ID
        Expected: Object is deleted from the database
        """
        db_client.add(obj1_user1)
        db_client.add(obj2_user1)
        db_client.delete(obj1_user1)
        assert db_client.get_all() == [obj2_user1]

    def test_incorrect_user(self, db_client, obj1_user1, obj1_user2):
        """
        Test deleting an object with an incorrect user ID
        Expected: ValueError is raised
        """
        db_client.add(obj1_user1)
        with pytest.raises(ValueError):
            db_client.delete(obj1_user2)
