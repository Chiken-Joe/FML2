class UserAsserts:
    @staticmethod
    def assert_user(user_json, expected_username=None, expected_email=None):
        assert "id" in user_json
        assert "username" in user_json
        assert "email" in user_json
        assert "is_active" in user_json
        assert "status" in user_json or user_json.get("status") is None  
        if expected_username:
            assert user_json["username"] == expected_username
        if expected_email:
            assert user_json["email"] == expected_email

class PostAsserts:
    @staticmethod
    def assert_post(post_json, expected_title=None, expected_content=None, expected_owner_id=None):
        assert "id" in post_json
        assert "title" in post_json
        assert "content" in post_json
        assert "owner_id" in post_json
        assert "created_at" in post_json
        assert "reactions" in post_json
        assert isinstance(post_json["reactions"], list)
        if expected_title:
            assert post_json["title"] == expected_title
        if expected_content:
            assert post_json["content"] == expected_content
        if expected_owner_id:
            assert post_json["owner_id"] == expected_owner_id

class CommentAsserts:
    @staticmethod
    def assert_comment(comment_json, expected_content=None, expected_post_id=None, expected_owner_id=None):
        assert "id" in comment_json
        assert "content" in comment_json
        assert "post_id" in comment_json
        assert "owner_id" in comment_json
        assert "created_at" in comment_json
        if expected_content:
            assert comment_json["content"] == expected_content
        if expected_post_id:
            assert comment_json["post_id"] == expected_post_id
        if expected_owner_id:
            assert comment_json["owner_id"] == expected_owner_id

class StatsAsserts:
    @staticmethod
    def assert_stats(stats_json):
        assert "total_users" in stats_json
        assert "total_posts" in stats_json
        assert "total_comments" in stats_json
        assert "most_common_reaction" in stats_json
        assert "most_active_procrastinator" in stats_json
        assert "average_comments_per_post" in stats_json
        assert isinstance(stats_json["total_users"], int)
        assert isinstance(stats_json["total_posts"], int)
        assert isinstance(stats_json["total_comments"], int)
        assert isinstance(stats_json["average_comments_per_post"], (int, float))