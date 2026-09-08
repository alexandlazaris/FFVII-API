from models import Save, Party, PartyMember
from schemas.party import *
from app import db
from uuid import UUID
TEST_USER_ID = UUID("00000000-0000-0000-0000-000000000001")



def test_can_get_existing_party(client, app):
    # seed Save data
    save_id = ""
    with app.app_context():
        data_1 = {"user_id": TEST_USER_ID, "location": "Midgar", "disc": 1}
        save_1 = Save(**data_1)
        db.session.add(save_1)
        db.session.commit()
        save_id = save_1.id

    party_id = ""
    # seed Party data
    with app.app_context():
        data_party = {"save_id": save_id}
        party_1 = Party(**data_party)
        db.session.add(party_1)
        db.session.commit()
        party_id = party_1.id

    # seed Party Members
    with app.app_context():
        data_members = {"party_id": party_id, "name": "Cloud"}
        party_members = PartyMember(**data_members)
        db.session.add(party_members)
        db.session.commit()

    response = client.get(
        f"/saves/{save_id}/party", headers={"Authorization": "Bearer test-token"}
    )

    json = response.get_json()
    assert response.status_code == 200
    assert json["party"][0]["name"] == "Cloud"
    assert json["id"] == party_id


def test_can_create_party_of_3(client, app):
    # seed Save data
    id_save: str = ""
    with app.app_context():
        data_1 = {"user_id": TEST_USER_ID, "location": "Midgar", "disc": 1}
        save_1 = Save(**data_1)
        db.session.add(save_1)
        db.session.commit()
        id_save = save_1.id

    body = [{"name": "Cloud"}, {"name": "Barret"}]
    response = client.post(
        f"/saves/{id_save}/party", json=body, headers={"Authorization": "Bearer test-token"}
    )
    json = response.get_json()
    assert json["party"][0]["name"] == body[0]["name"]
    assert json["party"][1]["name"] == body[1]["name"]
    assert response.status_code == 200

def test_cannot_create_party_with_duplicates(client, app):
    # seed Save data
    id_save: str = ""
    with app.app_context():
        data_1 = {"user_id": TEST_USER_ID, "location": "Midgar", "disc": 1}
        save_1 = Save(**data_1)
        db.session.add(save_1)
        db.session.commit()
        id_save = save_1.id

    body = [{"name": "Cloud"}, {"name": "Cloud"}]
    response = client.post(
        f"/saves/{id_save}/party", json=body, headers={"Authorization": "Bearer test-token"}
    )
    json = response.get_json()
    assert response.status_code == 409

def test_cannot_party_if_party_already_exists(client, app):
    # seed Save data
    save_id: str = ""
    with app.app_context():
        data_1 = {"user_id": TEST_USER_ID, "location": "Midgar", "disc": 1}
        save_1 = Save(**data_1)
        db.session.add(save_1)
        db.session.commit()
        save_id = save_1.id

    party_id = ""
    # seed Party data
    with app.app_context():
        data_party = {"save_id": save_id}
        party_1 = Party(**data_party)
        db.session.add(party_1)
        db.session.commit()
        party_id = party_1.id

    # seed Party Members
    with app.app_context():
        data_members = {"party_id": party_id, "name": "Cloud"}
        party_members = PartyMember(**data_members)
        db.session.add(party_members)
        db.session.commit()

    body = [{"name": "Cloud"}]
    response = client.post(
        f"/saves/{save_id}/party", json=body, headers={"Authorization": "Bearer test-token"}
    )
    json = response.get_json()
    assert response.status_code == 400

