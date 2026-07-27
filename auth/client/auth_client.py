import os
import logging
from supabase import create_client, Client

logger = logging.getLogger(__name__)


class AuthClient:
    def __init__(self):
        self.url: str | None = os.getenv("SUPABASE_URL")
        self.key: str | None = os.getenv("SUPABASE_KEY")
        self.auth_client: Client

    def client_setup(self):
        self.auth_client: Client = create_client(
            supabase_url=self.url or "", supabase_key=self.key or ""
        )
        logging.info("auth client created")

    def create_dummy_user(self):
        response = self.auth_client.auth.sign_in_anonymously(
            {"options": {"data": {"name": "anon_test_user"}}}
        )
        return response

    def signup(self, email: str, password: str):
        logger.info("signing up new user with password")
        return self.auth_client.auth.sign_up({"email": email, "password": password})

    def login(self, username: str, password: str):
        logger.info("logging in with password")
        return self.auth_client.auth.sign_in_with_password(
            {"email": username, "password": password}
        )

auth = AuthClient()
