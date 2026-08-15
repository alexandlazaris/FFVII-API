from models import Save
from app import db
import uuid


def test_get_save_by_id(client, app):
    id = ""
    with app.app_context():
        data_1 = {"user_id": uuid.uuid4(), "location": "Midgar", "disc": 1}
        save_1 = Save(**data_1)
        db.session.add(save_1)
        db.session.commit()
        id = save_1.id
    response = client.get(f"/save/{id}", headers={"Authorization": "Bearer test-token"})
    json = response.get_json()
    assert response.status_code == 200
    assert json["id"] == id
    assert json["location"] == "Midgar"


def test_delete_save_by_id(client, app):
    id = ""
    with app.app_context():
        data_1 = {"user_id": uuid.uuid4(), "location": "Midgar", "disc": 1}
        save_1 = Save(**data_1)
        db.session.add(save_1)
        db.session.commit()
        id = save_1.id
    response = client.delete(
        f"/save/{id}", headers={"Authorization": "Bearer fake-token"}
    )
    json = response.get_json()
    assert response.status_code == 200
    assert json["message"] == f"deleted {id}"
