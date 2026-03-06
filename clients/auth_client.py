from .base_client import BaseClient

class AuthClient(BaseClient):
    def login(self, email: str, password: str):
        payload = {"email": email, "password": password}
        return self._request("POST", "/auth/login", json=payload)

    def logout(self):
        return self._request("POST", "/auth/logout")

    def get_me(self):
        return self._request("GET", "/auth/me")

    def refresh_token(self):
        return self._request("POST", "/auth/refresh")