from models.auth.auth import (
    LoginResponse,
    LogoutResponse,
    SignUpResponse,
    SignUpConfirmedResponse,
)
import logging
from auth.client.auth_client import AuthClient

_auth_client = AuthClient()

logger = logging.getLogger(__name__)


def signup_with_email_password(email: str, password: str) -> SignUpResponse:
    response = _auth_client.signup(email, password)
    if response.user is None:
        raise RuntimeError("Expected session from email signup, returned Exception")
    return SignUpResponse(email=response.user.email)


def login_with_password(email: str, password: str) -> LoginResponse:
    response = _auth_client.login(email, password)
    if response.session is None:
        raise RuntimeError("Expected session from password login, returned Exception")
    return LoginResponse(
        access_token=response.session.access_token,
        refresh_token=response.session.refresh_token,
    )


def sign_out() -> LogoutResponse:
    _auth_client.sign_out()
    return LogoutResponse(result="log out complete")


def delete_account():
    print("TODO")


def confirm_user_sign(token_hash: str) -> SignUpConfirmedResponse:
    response = _auth_client.confirm_user_signup(token_hash)
    if response.user is None:
        raise RuntimeError("Expected signup confirmation, returned Exception")
    return SignUpConfirmedResponse(
        id=response.user.id,
        email=response.user.email,
        confirmed_at=response.user.confirmed_at,
    )
