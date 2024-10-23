import datetime as dt

import pytest

from lifehub.clients.db.user import APITokenRepository
from lifehub.models.user_old import APIToken


@pytest.fixture(scope="module")
def token_id1():
    return "api1"


@pytest.fixture(scope="module")
def token_id2():
    return "api2"


@pytest.fixture(scope="function")
def api_token1_user1(user1, token_id1):
    return APIToken(
        user_id=user1.id,
        api_id=token_id1,
        token="token1",
        expires_at=dt.datetime.now() + dt.timedelta(days=1),
    )


@pytest.fixture(scope="function")
def api_token1_user2(user2, token_id1):
    return APIToken(
        user_id=user2.id,
        api_id=token_id1,
        token="token1",
        expires_at=dt.datetime.now() + dt.timedelta(days=1),
    )


@pytest.fixture(scope="function")
def api_token2_user1(user1, token_id2):
    return APIToken(
        user_id=user1.id,
        api_id=token_id2,
        token="token2",
        expires_at=dt.datetime.now() + dt.timedelta(days=1),
    )


@pytest.fixture(scope="function")
def api_token2_user2(user2, token_id2):
    return APIToken(
        user_id=user2.id,
        api_id=token_id2,
        token="token2",
        expires_at=dt.datetime.now() + dt.timedelta(days=1),
    )


@pytest.fixture(scope="function")
def db_client(engine):
    APIToken.metadata.create_all(bind=engine)
    yield APITokenRepository()
    APIToken.metadata.drop_all(bind=engine)


def test_creation():
    """
    Test creating an APITokenRepository object
    Expected: Object is created
    """
    assert APITokenRepository()


class TestGetUserIDsWithTokens:
    def test_no_entries(self, db_client):
        """
        Test that when no entries are in the database, no users are returned
        """
        assert db_client.get_user_ids_with_tokens([]) == []

    def test_no_tokens(
        self,
        db_client,
        api_token1_user1,
        api_token1_user2,
        api_token2_user1,
        api_token2_user2,
    ):
        """
        Test that when no tokens are provided, no users are returned
        """
        db_client.add(api_token1_user1)
        db_client.add(api_token1_user2)
        db_client.add(api_token2_user1)
        db_client.add(api_token2_user2)
        assert db_client.get_user_ids_with_tokens([]) == []

    def test_single_token_all_users(
        self,
        db_client,
        user1,
        user2,
        token_id1,
        api_token1_user1,
        api_token2_user1,
        api_token1_user2,
    ):
        """
        Test that when a single token is provided, all users with that token are returned
        """
        db_client.add(api_token1_user1)
        db_client.add(api_token2_user1)
        db_client.add(api_token1_user2)
        assert len(db_client.get_user_ids_with_tokens([token_id1])) == 2
        assert user1.id in db_client.get_user_ids_with_tokens([token_id1])
        assert user2.id in db_client.get_user_ids_with_tokens([token_id1])

    def test_single_token_some_users(
        self, db_client, user1, token_id1, api_token1_user1, api_token2_user2
    ):
        """
        Test that when a single token is provided, only the users with that token are returned
        """
        db_client.add(api_token1_user1)
        db_client.add(api_token2_user2)
        assert len(db_client.get_user_ids_with_tokens([token_id1])) == 1
        assert user1.id in db_client.get_user_ids_with_tokens([token_id1])

    def test_single_token_no_users(
        self, db_client, token_id1, api_token2_user1, api_token2_user2
    ):
        """
        Test that when a single token is provided, no users are returned if they don't have that token
        """
        db_client.add(api_token2_user1)
        db_client.add(api_token2_user2)
        assert db_client.get_user_ids_with_tokens([token_id1]) == []

    def test_multiple_tokens_all_users(
        self,
        db_client,
        user1,
        user2,
        token_id1,
        token_id2,
        api_token1_user1,
        api_token1_user2,
        api_token2_user1,
        api_token2_user2,
    ):
        """
        Test that when multiple tokens are provided, all users with those tokens are returned
        """
        db_client.add(api_token1_user1)
        db_client.add(api_token1_user2)
        db_client.add(api_token2_user1)
        db_client.add(api_token2_user2)
        assert len(db_client.get_user_ids_with_tokens([token_id1, token_id2])) == 2
        assert user1.id in db_client.get_user_ids_with_tokens([token_id1, token_id2])
        assert user2.id in db_client.get_user_ids_with_tokens([token_id1, token_id2])

    def test_multiple_tokens_some_users(
        self,
        db_client,
        user1,
        token_id1,
        token_id2,
        api_token1_user1,
        api_token1_user2,
        api_token2_user1,
    ):
        """
        Test that when multiple tokens are provided, only the users with all tokens are returned
        """
        db_client.add(api_token1_user1)
        db_client.add(api_token1_user2)
        db_client.add(api_token2_user1)
        assert len(db_client.get_user_ids_with_tokens([token_id1, token_id2])) == 1
        assert user1.id in db_client.get_user_ids_with_tokens([token_id1, token_id2])

    def test_multiple_tokens_no_users(
        self,
        db_client,
        token_id1,
        token_id2,
        api_token1_user1,
        api_token2_user2,
    ):
        """
        Test that when multiple tokens are provided, no users are returned if they don't have all tokens
        """
        db_client.add(api_token1_user1)
        db_client.add(api_token2_user2)
        assert db_client.get_user_ids_with_tokens([token_id1, token_id2]) == []
