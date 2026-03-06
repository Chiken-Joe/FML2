import pytest
from asserts.response_asserts import ResponseAsserts as RA

def test_login_success(auth_client, create_user):
    user_id, user_data = create_user
    response = auth_client.login(user_data["email"], user_data["password"])
    RA.assert_status(response, 200)
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert "expires_in" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password(auth_client, create_user):
    user_id, user_data = create_user
    response = auth_client.login(user_data["email"], "wrongpassword")
    RA.assert_status(response, 401)
    RA.assert_error_message(response, "Неверный email или пароль. Или оба сразу. Попробуй еще раз.")

def test_login_nonexistent_user(auth_client):
    response = auth_client.login("nonexistent@example.com", "pass")
    RA.assert_status(response, 401)
    RA.assert_error_message(response, "Неверный email или пароль. Или оба сразу. Попробуй еще раз.")

def test_logout(auth_client, create_user):
    user_id, user_data = create_user
    login_resp = auth_client.login(user_data["email"], user_data["password"])
    token = login_resp.json()["access_token"]
    auth_client.set_auth_header(token)
    logout_resp = auth_client.logout()
    RA.assert_status(logout_resp, 200)
    me_resp = auth_client.get_me()
    RA.assert_status(me_resp, 401)

def test_get_me(auth_client, create_user):
    user_id, user_data = create_user
    login_resp = auth_client.login(user_data["email"], user_data["password"])
    token = login_resp.json()["access_token"]
    auth_client.set_auth_header(token)
    me_resp = auth_client.get_me()
    RA.assert_status(me_resp, 200)
    data = me_resp.json()
    assert data["id"] == user_id
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]

def test_refresh_token(auth_client, create_user):
    user_id, user_data = create_user
    login_resp = auth_client.login(user_data["email"], user_data["password"])
    old_token = login_resp.json()["access_token"]
    auth_client.set_auth_header(old_token)
    refresh_resp = auth_client.refresh_token()
    RA.assert_status(refresh_resp, 200)
    new_token_data = refresh_resp.json()
    assert "access_token" in new_token_data
    assert new_token_data["access_token"] != old_token
    auth_client.set_auth_header(old_token)
    me_resp = auth_client.get_me()
    RA.assert_status(me_resp, 401)
    auth_client.set_auth_header(new_token_data["access_token"])
    me_resp2 = auth_client.get_me()
    RA.assert_status(me_resp2, 200)