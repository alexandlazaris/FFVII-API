import pytest
from datetime import datetime
from unittest.mock import patch, Mock
from types import SimpleNamespace

from supabase import AuthApiError
from auth.auth_exceptions import SessionNotFound
from auth.user_exceptions import UserNotFound
from services.user.user_service import get_profile


@patch("services.user.user_service._auth_client")
def test_get_profile(mock_auth_client):
    dt = datetime.fromisoformat("2026-08-05T11:21:14.224888+00:00")
    mock_user = SimpleNamespace(
        id="58cf7031-16df-4cda-b728-fd5f86d8240",
        email="test@email.com",
        is_anonymous=False,
        last_sign_in_at=dt,
    )
    mock_auth_client.get_user.return_value = mock_user
    response = get_profile("test-token")
    assert response.user_id == mock_user.id
    assert response.email == mock_user.email
    assert response.is_anonymous == mock_user.is_anonymous
    assert response.last_sign_in_at == mock_user.last_sign_in_at


@patch("services.user.user_service._auth_client")
def test_get_profile_no_user(mock_auth_client):
    mock_auth_client.get_user.return_value = None
    with pytest.raises(UserNotFound):
        get_profile("test-token")


@patch("services.user.user_service._auth_client")
def test_auth_api_error(mock_auth_client):
    mock_error = Mock()
    mock_error.e.code = "user_not_found"
    mock_auth_client.get_user.side_effect = SessionNotFound
    with pytest.raises(SessionNotFound):
        get_profile("test-token")
