from auth.user_exceptions import UserNotFound
from models.user.user import GetUserResponse
import logging
from auth.client.auth_client import AuthClient
from uuid import UUID
from flask import g

_auth_client = AuthClient()

logger = logging.getLogger(__name__)


def get_profile(access_token: str) -> GetUserResponse:
    user = _auth_client.get_user(access_token)
    if user is None:
        raise UserNotFound("Error getting user. User not found.")
    return GetUserResponse(
        user_id=user.id,
        email=user.email,
        is_anonymous=user.is_anonymous,
        last_sign_in_at=user.last_sign_in_at,
    )


def get_user_id() -> UUID:
    user_id = UUID(g.user.user_id)
    return user_id
