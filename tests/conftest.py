import pytest
from app import create_app
from flask_migrate import upgrade
from db import db

@pytest.fixture
def app():
    app = create_app("sqlite:///:memory:")
    app.testing = True
    with app.app_context():
        upgrade()
        yield app
        db.session.remove()

@pytest.fixture
def client(app):
    return app.test_client()