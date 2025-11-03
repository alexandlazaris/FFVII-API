from models import MateriaModel
from app import db


def test_create_new_materia(client):
    body = [
        {"name": "Comet2", "type": "magic", "element": "non-elemental"},
    ]
    response = client.post("/materia", json=body)
    assert response.status_code == 201
    json = response.get_json()
    assert json[0]["name"] == body[0]["name"]
    assert json[0]["type"] == body[0]["type"]
    assert json[0]["element"] == body[0]["element"]


def test_get_materia_using_filter_type(client, app):
    data = [
        {"id": 1, "name": "Comet", "type": "magic", "element": "non-elemental"},
        {"id": 2, "name": "Barrier", "type": "magic", "element": None},
        {"id": 3, "name": "Time", "type": "magic", "element": "time"},
        {"id": 4, "name": "test_name", "type": "test_type", "element": "test_element"},
    ]

    with app.app_context():
        for d in data:
            new_materia = MateriaModel(**d)
            db.session.add(new_materia)
        db.session.commit()

    response = client.get("/materia?type=test_type")
    assert response.status_code == 200
    json = response.get_json()
    assert json[0]["name"] == data[3]["name"]
    assert json[0]["type"] == data[3]["type"]
    assert json[0]["element"] == data[3]["element"]


def test_get_materia_using_filter_element(client, app):
    data = [
        {"id": 1, "name": "Comet", "type": "magic", "element": "non-elemental"},
        {"id": 2, "name": "Barrier", "type": "magic", "element": None},
        {"id": 3, "name": "Time", "type": "magic", "element": "time"},
        {"id": 4, "name": "test_name", "type": "test_type", "element": "test_element"},
    ]

    with app.app_context():
        for d in data:
            new_materia = MateriaModel(**d)
            db.session.add(new_materia)
        db.session.commit()

    response = client.get("/materia?element=test_element")
    assert response.status_code == 200
    json = response.get_json()
    assert json[0]["name"] == data[3]["name"]
    assert json[0]["type"] == data[3]["type"]
    assert json[0]["element"] == data[3]["element"]
