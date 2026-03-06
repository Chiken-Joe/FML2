from .base_client import BaseClient

class UserClient(BaseClient):
    def create_user(self, username: str, email: str, password: str):
        return self._request("POST", "/users/", json={"username": username, "email": email, "password": password})

    def get_all_users(self):
        return self._request("GET", "/users/")

    def get_user(self, user_id: str):
        return self._request("GET", f"/users/{user_id}")

    def update_status(self, user_id: str, status: str):
        return self._request("PUT", f"/users/{user_id}/status", params={"status": status})

    def delete_user(self, user_id: str):
        return self._request("DELETE", f"/users/{user_id}")