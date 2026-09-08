import pytest
from app import create_app
from db import db
from unittest.mock import patch
from uuid import UUID
from auth.jwt.principal import AuthenticatedUser

import os

db_name = os.environ["POSTGRES_DB"]
username = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]

os.environ["DATABASE_URL"] = (
    f"postgresql+psycopg://{username}:{password}@localhost:5432/{db_name}"
)


@pytest.fixture
def app():
    app = create_app()
    app.testing = True
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


TEST_USER_ID = UUID("00000000-0000-0000-0000-000000000001")


@pytest.fixture(autouse=True)
def mock_auth():
    with patch("auth.jwt.decorators.verify_access_token") as mock:
        mock.return_value = AuthenticatedUser(
            user_id=str(TEST_USER_ID),
            email="test@example.com",
        )
        yield mock
