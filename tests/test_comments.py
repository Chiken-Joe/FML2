import pytest
from asserts.response_asserts import ResponseAsserts as RA
from asserts.model_asserts import CommentAsserts

def test_create_comment_success(comment_client, create_post, create_user, random_comment_data):
    post_id, owner_id, post_data = create_post
    user_id2, user_data2 = create_user
    response = comment_client.create_comment(post_id, user_id2, random_comment_data["content"])
    RA.assert_status(response, 201)
    RA.assert_content_type(response)
    data = response.json()
    CommentAsserts.assert_comment(data, random_comment_data["content"], post_id, user_id2)

def test_create_comment_post_not_found(comment_client, create_user, random_comment_data):
    user_id, user_data = create_user
    fake_post_id = "00000000-0000-0000-0000-000000000000"
    response = comment_client.create_comment(fake_post_id, user_id, random_comment_data["content"])
    RA.assert_status(response, 404)
    RA.assert_error_message(response, "Пост не найден. Мысль потеряна, как и все наши мечты.")

def test_create_comment_user_not_found(comment_client, create_post, random_comment_data):
    post_id, owner_id, post_data = create_post
    fake_user_id = "00000000-0000-0000-0000-000000000000"
    response = comment_client.create_comment(post_id, fake_user_id, random_comment_data["content"])
    RA.assert_status(response, 404)
    RA.assert_error_message(response, "Пользователь не найден. Нельзя комментировать из небытия.")

def test_get_comments(comment_client, create_post, create_user, random_comment_data):
    post_id, owner_id, post_data = create_post
    user_id2, user_data2 = create_user
    comment_client.create_comment(post_id, user_id2, random_comment_data["content"])
    response = comment_client.get_comments(post_id)
    RA.assert_status(response, 200)
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    CommentAsserts.assert_comment(data[0], random_comment_data["content"], post_id, user_id2)

def test_get_comments_empty(comment_client, create_post):
    post_id, owner_id, post_data = create_post
    response = comment_client.get_comments(post_id)
    RA.assert_status(response, 200)
    data = response.json()
    assert data == []

def test_get_comments_post_not_found(comment_client):
    fake_post_id = "00000000-0000-0000-0000-000000000000"
    response = comment_client.get_comments(fake_post_id)
    RA.assert_status(response, 404)
    RA.assert_error_message(response, "Пост не существует, как и объективность.")