import requests
from config import BASE_URL
from utils.logger import log_response

class BaseClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.hooks["response"] = [log_response]

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        return self.session.request(method, url, **kwargs)

    def set_auth_header(self, token: str):
        self.session.headers.update({"Authorization": f"Bearer {token}"})