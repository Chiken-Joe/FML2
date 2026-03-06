from .base_client import BaseClient

class CommentClient(BaseClient):
    def create_comment(self, post_id: str, user_id: str, content: str):
        payload = {"content": content}
        return self._request("POST", f"/posts/{post_id}/comments/", params={"user_id": user_id}, json=payload)

    def get_comments(self, post_id: str):
        return self._request("GET", f"/posts/{post_id}/comments/")