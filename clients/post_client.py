from .base_client import BaseClient

class PostClient(BaseClient):
    def create_post(self, user_id: str, title: str, content: str):
        payload = {"title": title, "content": content}
        return self._request("POST", "/posts/", params={"user_id": user_id}, json=payload)

    def get_all_posts(self):
        return self._request("GET", "/posts/")

    def get_post(self, post_id: str):
        return self._request("GET", f"/posts/{post_id}")

    def react_to_post(self, post_id: str, user_id: str, reaction_type: str):
        params = {"user_id": user_id, "reaction_type": reaction_type}
        return self._request("POST", f"/posts/{post_id}/react", params=params)

    def delete_post(self, post_id: str):
        return self._request("DELETE", f"/posts/{post_id}")