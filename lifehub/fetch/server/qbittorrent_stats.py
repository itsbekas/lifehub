from lifehub.fetch.base import BaseFetcher
from lifehub.lib.api import QBittorrentAPIClient
from lifehub.lib.models.server import QBittorrentStats


class QBittorrentStatsFetcher(BaseFetcher):
    table_id = "qbitstats"

    def fetch_data(self):
        qb = QBittorrentAPIClient.get_instance()

        main_data = qb.get_main_data()

        state = main_data.server_state

        stats = QBittorrentStats(
            alltime_dl=state.alltime_dl,
            alltime_ul=state.alltime_ul,
            alltime_ratio=state.global_ratio,
        )

        self.session.add(stats)