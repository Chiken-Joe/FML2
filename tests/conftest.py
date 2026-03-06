import pytest
from clients.auth_client import AuthClient
from clients.user_client import UserClient
from clients.post_client import PostClient
from clients.comment_client import CommentClient
from clients.stats_client import StatsClient
from fixtures.data_factory import (
    random_email, random_username, random_password,
    random_post_title, random_post_content, random_comment, random_status
)

@pytest.fixture(scope="session")
def auth_client():
    return AuthClient()

@pytest.fixture(scope="session")
def user_client():
    return UserClient()

@pytest.fixture(scope="session")
def post_client():
    return PostClient()

@pytest.fixture(scope="session")
def comment_client():
    return CommentClient()

@pytest.fixture(scope="session")
def stats_client():
    return StatsClient()

@pytest.fixture
def random_user_data():
    return {
        "username": random_username(),
        "email": random_email(),
        "password": random_password()
    }

@pytest.fixture
def random_post_data():
    return {
        "title": random_post_title(),
        "content": random_post_content()
    }

@pytest.fixture
def random_comment_data():
    return {"content": random_comment()}

@pytest.fixture
def random_status_value():
    return random_status()

@pytest.fixture
def create_user(user_client, random_user_data):
    response = user_client.create_user(**random_user_data)
    assert response.status_code == 201
    user = response.json()
    return user["id"], random_user_data

@pytest.fixture
def create_post(user_client, post_client, create_user):
    user_id, user_data = create_user
    post_data = {
        "title": random_post_title(),
        "content": random_post_content()
    }
    response = post_client.create_post(user_id, post_data["title"], post_data["content"])
    assert response.status_code == 201
    post = response.json()
    return post["id"], user_id, post_data