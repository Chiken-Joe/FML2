from .base_client import BaseClient

class StatsClient(BaseClient):
    def get_stats(self):
        return self._request("GET", "/stats/")