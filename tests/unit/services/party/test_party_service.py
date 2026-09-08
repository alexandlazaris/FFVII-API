from models import Save
from schemas.party import *
from services.party_service import *
from app import db
from uuid import UUID
from flask import g
from auth.jwt.principal import AuthenticatedUser

TEST_USER_ID = UUID("00000000-0000-0000-0000-000000000001")


def test_create_party_can_create_party(app):
    with app.app_context():
    # form user obj
        g.user = AuthenticatedUser(
            user_id=str(TEST_USER_ID),
            email="test@example.com",
        )

    # seed Save data
        save_id: str = ""
        data_1 = {"user_id": TEST_USER_ID, "location": "Midgar", "disc": 1}
        save_1 = Save(**data_1)
        db.session.add(save_1)
        db.session.commit()
        save_id = save_1.id

        body = [{"name": "Cloud"}, {"name": "Barret"}]
        result = create_party(body, save_id)
        assert result.party.__len__() == 2
        assert result.party[0].name == "Cloud"
        assert type(result.party[0].level) is int
        assert type(result.id) is UUID


# TODO: add tests for remaining party_service functions
