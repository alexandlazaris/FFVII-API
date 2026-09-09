from unittest.mock import patch
from auth.auth_exceptions import *
from models.auth.auth import *


@patch("resources.auth.auth.signup_with_email_password")
def test_signup_with_email_password_success(mock_signup, client):
    mock_signup.return_value = SignUpResponse(
        email="test@example.com",
    )
    body = {"email": "test@example.com", "password": "password"}
    response = client.post(
        "/auth/signup", json=body, headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
    json = response.get_json()
    assert json["email"] == "test@example.com"

@patch("resources.auth.auth.signup_with_email_password")
def test_signup_with_email_password_existing_email(mock_signup, client):
    mock_signup.side_effect = EmailExistsError()
    body = {"email": "test@example.com", "password": "password"}
    response = client.post(
        "/auth/signup", json=body, headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 401
    json = response.get_json()
    assert json["message"] == "Email already exists"

@patch("resources.auth.auth.login_with_password")
def test_login_success(mock_login, client):
    mock_login.return_value = LoginResponse(access_token="access", refresh_token="refresh")
    body = {"email": "test@example.com", "password": "password"}
    response = client.post(
        "/auth/login", json=body, headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
    json = response.get_json()
    assert json["access_token"] == "access"
    assert json["refresh_token"] == "refresh"

@patch("resources.auth.auth.login_with_password")
def test_login_email_not_confirmed(mock_login, client):
    mock_login.side_effect = EmailNotConfirmedError()
    body = {"email": "test@example.com", "password": "password"}
    response = client.post(
        "/auth/login", json=body, headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 401
    json = response.get_json()
    assert json["message"] == "Email not confirmed"

@patch("resources.auth.auth.login_with_password")
def test_login_incorrect_credentials(mock_login, client):
    mock_login.side_effect = InvalidCredentialsError()
    body = {"email": "test@example.com", "password": "password"}
    response = client.post(
        "/auth/login", json=body, headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 401
    json = response.get_json()
    assert json["message"] == "Invalid credentials"

@patch("resources.auth.auth.sign_out")
def test_logout_success(mock_login, client):
    mock_login.return_value = LogoutResponse(result="")
    response = client.post(
        "/auth/logout", headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 204

@patch("resources.auth.auth.sign_out")
def test_logout_session_not_found(mock_login, client):
    mock_login.side_effect = SessionNotFound()
    response = client.post(
        "/auth/logout", headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 401
    json = response.get_json()
    assert json["message"] == "User session not found"
