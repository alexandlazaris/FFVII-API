from models import Save
from schemas.party import *
from services.party_service import *
from app import db
import uuid


def test_create_party_can_create_party(app):
    # seed Save data
    save_id: str = ""
    with app.app_context():
        data_1 = {"user_id": uuid.uuid4(), "location": "Midgar", "disc": 1}
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

# test to get party & party members