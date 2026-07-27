from models import Save
from app import db

def test_create_save(client):
    body = {"location": "mideel"}
    response = client.post(
        "/save", headers={"Authorization": "Bearer test-token"}, json=body
    )
    assert response.status_code == 201
    json = response.get_json()
    assert json["id"] is not None
    assert json["location"] == "mideel"


def test_get_save_by_id(client, app):
    with app.app_context():
        save_1 = Save(id="123", location="midgar")
        db.session.add(save_1)
        db.session.commit()
    response = client.get("/save/123", headers={"Authorization": "Bearer test-token"})
    json = response.get_json()
    assert response.status_code == 200
    assert json["id"] == "123"
    assert json["location"] == "midgar"

def test_delete_save_by_id(client, app):
    with app.app_context():
        save_1 = Save(id="999", location="midgar")
        db.session.add(save_1)
        db.session.commit()
    response = client.delete(
        "/save/999", headers={"Authorization": "Bearer fake-token"}
    )
    json = response.get_json()
    assert response.status_code == 200
    assert json["message"] == "deleted 999"
