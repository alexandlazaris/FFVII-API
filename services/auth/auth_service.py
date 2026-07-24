from flask_smorest import abort
from pydantic import ValidationError
from supabase import AuthApiError
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.auth.auth import LoginResponse, SignupRequest, LoginRequest, SignUpResponse
import json
from flask import jsonify
import logging
from auth.auth_client import auth

logger = logging.getLogger(__name__)

# TODO: split these errors into a separate module

class EmailExistsError(Exception):
    pass

class EmailRateLimitExceededError(Exception):
    pass

class EmailNotConfirmedError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass


def signup_with_email_password(email: str, password: str) -> SignUpResponse:
    try:
        response = auth.signup(email, password)
        if response.session is None:
            raise RuntimeError("Expected session from email signup, returned Exception")
        return SignUpResponse(
            email=response.session.user.user_metadata["email"],
            email_verified=response.session.user.user_metadata["email_verified"],
        )
    except AuthApiError as e:
        match e.code:
            case "email_exists":
                raise EmailExistsError()
            case "over_email_send_rate_limit":
                raise EmailRateLimitExceededError()
            case _:
                raise

def get_error_metadata(e:AuthApiError):
    print (e, flush=True)
    print (e.message, flush=True)
    print (e.code, flush=True)
    print (e.status, flush=True)

def login_with_password(email: str, password: str) -> LoginResponse:
    try:
        response = auth.login(email, password)
        if response.session is None:
            raise RuntimeError(
                "Expected session from password login, returned Exception"
            )
        return LoginResponse(
            access_token=response.session.access_token,
            refresh_token=response.session.refresh_token,
        )
    except AuthApiError as e:
        match e.code:
            case "email_not_confirmed":
                raise EmailNotConfirmedError()
            case "invalid_credentials":
                raise InvalidCredentialsError()
            case _:
                raise

def logout():
    print("TODO")

def delete_account():
    print("TODO")