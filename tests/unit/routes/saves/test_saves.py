from models import Save
from app import db
from uuid import UUID
TEST_USER_ID = UUID("00000000-0000-0000-0000-000000000001")


def test_get_save_by_id(client, app):
    save_id: str = ""
    with app.app_context():
        data_1 = {"user_id": TEST_USER_ID, "location": "Midgar", "disc": 1}
        save_1 = Save(**data_1)
        db.session.add(save_1)
        db.session.commit()
        save_id = save_1.id 
    response = client.get(
        f"/saves/{save_id}", headers={"Authorization": "Bearer test-token"}
    )
    json = response.get_json()
    assert response.status_code == 200
    assert json["disc"] == 1
    assert json["location"] == "Midgar"
    assert json["party"]["id"] == None
    assert json["party"]["lead"] == None
    assert json["party"]["members"] == None

def test_get_all_saves(client, app):
    with app.app_context():
        data_1 = {"user_id": TEST_USER_ID, "location": "Midgar", "disc": 1}
        data_2 = {"user_id": TEST_USER_ID, "location": "Temple of the Ancients", "disc": 2}

        save_1 = Save(**data_1)
        save_2 = Save(**data_2)
        db.session.add(save_1)
        db.session.add(save_2)
        db.session.commit()
    response = client.get("/saves", headers={"Authorization": "Bearer test-token"})
    json = response.get_json()
    assert response.status_code == 200
    assert len(json["saves"])  == 2


def test_delete_all_saves(client, app):
    with app.app_context():
        data_1 = {"user_id": TEST_USER_ID, "location": "Midgar", "disc": 1}
        data_2 = {
            "user_id": TEST_USER_ID,
            "location": "Temple of the Ancients",
            "disc": 2,
        }

        save_1 = Save(**data_1)
        save_2 = Save(**data_2)
        db.session.add(save_1)
        db.session.add(save_2)
        db.session.commit()
    response = client.delete("/saves", headers={"Authorization": "Bearer test-token"})
    json = response.get_json()
    assert response.status_code == 200
    assert json["message"] == "deleted 2 save(s)"
