import uuid

import pytest

from lifehub.clients.db.server import QBittorrentStatsRepository
from lifehub.providers.qbittorrent.schema import QBittorrentStats


@pytest.fixture(scope="module")
def user_id():
    return uuid.uuid4()


@pytest.fixture(scope="function")
def db_client(engine, user_id):
    QBittorrentStats.metadata.create_all(bind=engine)
    yield QBittorrentStatsRepository(user_id)
    QBittorrentStats.metadata.drop_all(bind=engine)


def test_creation(db_client):
    """
    Test creating a QBittorrentStatsRepository object
    Expected: Object is created
    """
    assert db_client
