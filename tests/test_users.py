import pytest
from asserts.response_asserts import ResponseAsserts as RA
from asserts.model_asserts import UserAsserts

def test_create_user_success(user_client, random_user_data):
    response = user_client.create_user(**random_user_data)
    RA.assert_status(response, 201)
    RA.assert_content_type(response)
    data = response.json()
    UserAsserts.assert_user(data, random_user_data["username"], random_user_data["email"])
    assert data["is_active"] is True
    assert data["status"] is None

def test_create_user_duplicate_email(user_client, create_user):
    user_id, user_data = create_user
    response = user_client.create_user(user_data["username"] + "2", user_data["email"], "newpass")
    RA.assert_status(response, 400)
    RA.assert_error_message(response, "Эта почта уже занята кем-то более удачливым.")

def test_create_user_missing_field(user_client, random_user_data):
    payload = random_user_data.copy()
    del payload["username"]
    response = user_client._request("POST", "/users/", json=payload)
    RA.assert_status(response, 422)

def test_get_all_users(user_client, create_user):
    response = user_client.get_all_users()
    RA.assert_status(response, 200)
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_user_by_id(user_client, create_user):
    user_id, user_data = create_user
    response = user_client.get_user(user_id)
    RA.assert_status(response, 200)
    UserAsserts.assert_user(response.json(), user_data["username"], user_data["email"])

def test_get_user_not_found(user_client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = user_client.get_user(fake_id)
    RA.assert_status(response, 404)
    RA.assert_error_message(response, "Пользователь не найден. Возможно, он обрёл свободу.")

def test_update_status(user_client, create_user, random_status_value):
    user_id, user_data = create_user
    response = user_client.update_status(user_id, random_status_value)
    RA.assert_status(response, 200)
    data = response.json()
    assert data["status"] == random_status_value

def test_update_status_invalid_value(user_client, create_user):
    user_id, user_data = create_user
    response = user_client.update_status(user_id, "invalid_status")
    RA.assert_status(response, 422)

def test_delete_user(user_client, create_user):
    user_id, user_data = create_user
    response = user_client.delete_user(user_id)
    RA.assert_status(response, 204)
    get_resp = user_client.get_user(user_id)
    RA.assert_status(get_resp, 404)

def test_delete_user_not_found(user_client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = user_client.delete_user(fake_id)
    RA.assert_status(response, 404)
    RA.assert_error_message(response, "Нельзя удалить того, кого не существует. Философия, однако.")