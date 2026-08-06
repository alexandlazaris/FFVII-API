import os
import logging
from typing import Optional
from supabase import SupabaseException, create_client, Client
from gotrue.errors import AuthApiError
from auth.auth_exceptions import *
from auth.user_exceptions import *
from gotrue.types import AuthResponse, User

logger = logging.getLogger(__name__)


class AuthClient:
    def __init__(self):
        self._url = os.environ["SUPABASE_URL"]
        self._key = os.environ["SUPABASE_KEY"]

    def _client(self) -> Client:
        try:
            """
            Return a new supabase auth client instance
            """
            return create_client(supabase_url=self._url, supabase_key=self._key)
        except SupabaseException as e:
            raise AuthConfigurationError() from e

    def create_dummy_user(self):
        client = self._client()
        response = client.auth.sign_in_anonymously(
            {"options": {"data": {"name": "anon_test_user"}}}
        )
        return response

    def signup(self, email: str, password: str) -> AuthResponse:
        client = self._client()
        try:
            result = client.auth.sign_up({"email": email, "password": password})
            return result
        except AuthApiError as e:
            match e.code:
                case "email_exists":
                    raise EmailExistsError()
                case "over_email_send_rate_limit":
                    raise EmailRateLimitExceededError()
                case _:
                    raise

    def login(self, username: str, password: str) -> AuthResponse:
        client = self._client()
        try:
            response = client.auth.sign_in_with_password(
                {"email": username, "password": password}
            )
            return response
        except AuthApiError as e:
            match e.code:
                case "email_not_confirmed":
                    raise EmailNotConfirmedError()
                case "invalid_credentials":
                    raise InvalidCredentialsError()
                case _:
                    raise

    def sign_out(self):
        client = self._client()
        try:
            client.auth.sign_out()
            return {"result": "sign out complete"}
        except AuthApiError as e:
            match e.code:
                case "session_not_found":
                    raise SessionNotFound()
                case _:
                    raise

    def get_user(self, access_token:str) -> User:
        client = self._client()
        try:
            response = client.auth.get_user(access_token)
            if response is None or response.user is None:
                # TODO: not totally convinced if error should be caught here or in respective service
                # TODO: check if this prints anything useful
                raise UserNotFound()
            return response.user
        except AuthApiError as e:
            match e.code:
                case "user_not_found":
                    raise UserNotFound()
                case _:
                    raise