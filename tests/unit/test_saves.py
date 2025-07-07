from models import Save
from app import db

def test_create_save(client):
    body = {"location": "mideel"}
    response = client.post("/saves", json=body)
    assert response.status_code == 201
    json = response.get_json()
    assert json["id"] is not None
    assert json["location"] == "mideel"

def test_get_all_saves(client, app):
    with app.app_context():
        save_1 = Save(location="midgar")
        save_2 = Save(location="gongaga")
        db.session.add(save_1)
        db.session.add(save_2)
        db.session.commit()
    response = client.get("/saves")
    assert response.status_code == 200
    json = response.get_json()
    assert len(json) == 2

def test_delete_all_saves(client, app):
    with app.app_context():
        save_1 = Save(location="midgar")
        save_2 = Save(location="midgar")
        db.session.add(save_1)
        db.session.add(save_2)
        db.session.commit()
    response = client.delete("/saves")
    assert response.status_code == 200
    json = response.get_json()
    assert json["message"] == "deleted 2 save file/s"

def test_get_save_by_id(client, app):
    with app.app_context():
        save_1 = Save(id="123",location="midgar")
        db.session.add(save_1)
        db.session.commit()
    response = client.get("/saves/123")
    json = response.get_json()
    assert response.status_code == 200
    assert json["id"] == "123"
    assert json["location"] == "midgar"

def test_delete_save_by_id(client, app):
    with app.app_context():
        save_1 = Save(id="999",location="midgar")
        db.session.add(save_1)
        db.session.commit()
    response = client.delete("/saves/999")
    json = response.get_json()
    assert response.status_code == 200
    assert json["message"] == "deleted 999"