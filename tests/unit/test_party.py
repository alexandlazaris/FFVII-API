from models import Save, Party
from app import db

def test_create_party_of_3(client, app):
    with app.app_context():
        save_1 = Save(id="123", location="gongaga")
        db.session.add(save_1)
        db.session.commit()
    body = [{"name": "Barret"}, {"name": "Cid"}, {"name": "Cait Sith"}]
    response = client.post(
        "/party/123", json=body
    )    
    json = response.get_json()
    assert response.status_code == 201
    assert len(json) == 3
    assert json[0]["name"] == body[0]["name"]
    assert json[1]["name"] == body[1]["name"]
    assert json[2]["name"] == body[2]["name"]


def test_get_party_by_save_id(client, app):
    with app.app_context():
        party_member_1 = Party(id="1", name="Cloud", save_id="999")
        party_member_2 = Party(id="2", name="Tifa", save_id="999")
        party_member_3 = Party(id="3", name="Cait Sith", save_id="999")
        db.session.add(party_member_1)
        db.session.add(party_member_2)
        db.session.add(party_member_3)
        db.session.commit()
    response = client.get("/party/999")
    json = response.get_json()
    assert response.status_code == 200
    assert len(json) == 3

def test_update_party(client, app):
    with app.app_context():
        save_1 = Save(id="123", location="gongaga")
        db.session.add(save_1)
        party_member_1 = Party(id="1", name="Cloud", save_id="999")
        db.session.add(party_member_1)
        db.session.commit()
    body = [{"name": "Barret"}]
    response = client.put(
        "/party/123", json=body
    )    
    json = response.get_json()
    assert response.status_code == 200
    assert len(json) == 1
    assert json[0]["name"] == body[0]["name"]