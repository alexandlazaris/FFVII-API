import pytest
from app import create_app
from db import db
from unittest.mock import patch

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


@pytest.fixture(autouse=True)
def mock_auth():
    with patch("auth.jwt.decorators.verify_access_token") as mock:
        mock.return_value = {
        "sub": "test_user_123",
        "email": "test@example.com",
    }
        yield mock