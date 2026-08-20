from datetime import datetime
from unittest.mock import patch
from models.user.user import GetUserResponse

@patch("resources.user.user.get_profile")
def test_get_profile_success(mock_get_profile, client):
    dt = datetime.fromisoformat("2026-08-05T11:21:14.224888+00:00")
    mock_get_profile.return_value = GetUserResponse(
        user_id="1",
        email="test@example.com",
        is_anonymous=False,
        last_sign_in_at=dt
    )
    response = client.get(
        "/user/profile", headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
    json = response.get_json()
    assert json['user_id'] == "1"
    assert json['email'] == "test@example.com"
    assert json['is_anonymous'] == False
    assert json['last_sign_in_at'] == dt.isoformat()
