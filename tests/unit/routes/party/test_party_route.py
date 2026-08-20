from models import Save, Party, PartyMember
from schemas.party import *
from app import db
import uuid


def test_can_get_existing_party(client, app):
    # seed Save data
    id_save: str = ""
    with app.app_context():
        data_1 = {"user_id": uuid.uuid4(), "location": "Midgar", "disc": 1}
        save_1 = Save(**data_1)
        db.session.add(save_1)
        db.session.commit()
        id_save = save_1.id

    # seed Party data
    with app.app_context():
        data_party = {"save_id": id_save}
        party_1 = Party(**data_party)
        db.session.add(party_1)
        db.session.commit()

    response = client.get(f"/party/{id_save}")
    json = response.get_json()
    assert response.status_code == 200
    assert len(json) == 1

def test_can_create_party_of_3(client, app):
    # seed Save data
    id_save: str = ""
    with app.app_context():
        data_1 = {"user_id": uuid.uuid4(), "location": "Midgar", "disc": 1}
        save_1 = Save(**data_1)
        db.session.add(save_1)
        db.session.commit()
        id_save = save_1.id

    body = [{"name": "Cloud"}, {"name": "Barret"}]
    response = client.post(f"/party/{id_save}", json=body)
    json = response.get_json()
    
    assert json[0]["name"] == "Cloud"
    assert json[1]["name"] == "Barret"
    assert response.status_code == 200
