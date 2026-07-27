from models import Save
from app import db

def test_get_all_saves(client, app):
    with app.app_context():
        save_1 = Save(location="midgar")
        save_2 = Save(location="gongaga")
        db.session.add(save_1)
        db.session.add(save_2)
        db.session.commit()
    response = client.get("/saves", headers={"Authorization": "Bearer test-token"})
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
    response = client.delete("/saves", headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 200
    json = response.get_json()
    assert json["message"] == "deleted 2 save(s)"
