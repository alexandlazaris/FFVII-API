from models import Save
from app import db
import uuid

def test_get_all_saves(client, app):
    with app.app_context():
        data_1 = {"user_id": uuid.uuid4(), "location": "Midgar", "disc": 1}
        data_2 = {"user_id": uuid.uuid4(), "location": "Temple of the Ancients", "disc": 2}
        
        save_1 = Save(**data_1)
        save_2 = Save(**data_2)
        db.session.add(save_1)
        db.session.add(save_2)
        db.session.commit()
    response = client.get("/saves", headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 200
    json = response.get_json()
    assert len(json) == 2

def test_delete_all_saves(client, app):
    with app.app_context():
        data_1 = {"user_id": uuid.uuid4(), "location": "Midgar", "disc": 1}
        data_2 = {"user_id": uuid.uuid4(), "location": "Temple of the Ancients", "disc": 2}
        
        save_1 = Save(**data_1)
        save_2 = Save(**data_2)
        db.session.add(save_1)
        db.session.add(save_2)
        db.session.commit()
    response = client.delete("/saves", headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 200
    json = response.get_json()
    assert json["message"] == "deleted 2 save(s)"
