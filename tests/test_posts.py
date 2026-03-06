import pytest
from asserts.response_asserts import ResponseAsserts as RA
from asserts.model_asserts import PostAsserts

def test_create_post_success(post_client, create_user, random_post_data):
    user_id, user_data = create_user
    response = post_client.create_post(user_id, random_post_data["title"], random_post_data["content"])
    RA.assert_status(response, 201)
    RA.assert_content_type(response)
    data = response.json()
    PostAsserts.assert_post(data, random_post_data["title"], random_post_data["content"], user_id)
    assert data["reactions"] == []

def test_create_post_user_not_found(post_client, random_post_data):
    fake_user_id = "00000000-0000-0000-0000-000000000000"
    response = post_client.create_post(fake_user_id, random_post_data["title"], random_post_data["content"])
    RA.assert_status(response, 404)
    RA.assert_error_message(response, "Нельзя постить от имени несуществующего пользователя. Это уже шизофрения.")

def test_get_all_posts(post_client, create_post):
    post_id, user_id, post_data = create_post
    response = post_client.get_all_posts()
    RA.assert_status(response, 200)
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_post_by_id(post_client, create_post):
    post_id, user_id, post_data = create_post
    response = post_client.get_post(post_id)
    RA.assert_status(response, 200)
    PostAsserts.assert_post(response.json(), post_data["title"], post_data["content"], user_id)

def test_get_post_not_found(post_client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = post_client.get_post(fake_id)
    RA.assert_status(response, 404)
    RA.assert_error_message(response, "Пост не найден. Наверное, его удалили из-за чрезмерного оптимизма.")

def test_react_to_post_add(post_client, create_post, create_user):
    post_id, owner_id, post_data = create_post
    user_id2, user_data2 = create_user
    response = post_client.react_to_post(post_id, user_id2, "sigh")
    RA.assert_status(response, 200)
    data = response.json()
    reactions = data["reactions"]
    assert len(reactions) == 1
    assert reactions[0]["user_id"] == user_id2
    assert reactions[0]["type"] == "sigh"

def test_react_to_post_change(post_client, create_post, create_user):
    post_id, owner_id, post_data = create_post
    user_id2, user_data2 = create_user
    post_client.react_to_post(post_id, user_id2, "sigh")
    response = post_client.react_to_post(post_id, user_id2, "facepalm")
    RA.assert_status(response, 200)
    data = response.json()
    reactions = data["reactions"]
    assert len(reactions) == 1
    assert reactions[0]["user_id"] == user_id2
    assert reactions[0]["type"] == "facepalm"

def test_react_to_post_remove(post_client, create_post, create_user):
    post_id, owner_id, post_data = create_post
    user_id2, user_data2 = create_user
    post_client.react_to_post(post_id, user_id2, "sigh")
    response = post_client.react_to_post(post_id, user_id2, "sigh")
    RA.assert_status(response, 200)
    data = response.json()
    assert data["reactions"] == []

def test_react_post_not_found(post_client, create_user):
    user_id, user_data = create_user
    fake_post_id = "00000000-0000-0000-0000-000000000000"
    response = post_client.react_to_post(fake_post_id, user_id, "sigh")
    RA.assert_status(response, 404)
    RA.assert_error_message(response, "Пост не найден. Реагировать на пустоту бессмысленно.")

def test_react_user_not_found(post_client, create_post):
    post_id, owner_id, post_data = create_post
    fake_user_id = "00000000-0000-0000-0000-000000000000"
    response = post_client.react_to_post(post_id, fake_user_id, "sigh")
    RA.assert_status(response, 404)
    RA.assert_error_message(response, "Пользователь не найден. Призракам реакции не положены.")

def test_delete_post(post_client, create_post):
    post_id, user_id, post_data = create_post
    response = post_client.delete_post(post_id)
    RA.assert_status(response, 204)
    get_resp = post_client.get_post(post_id)
    RA.assert_status(get_resp, 404)

def test_delete_post_not_found(post_client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = post_client.delete_post(fake_id)
    RA.assert_status(response, 404)
    RA.assert_error_message(response, "Удалять нечего. Мир и так пуст.")