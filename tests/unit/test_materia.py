from models import MateriaModel
from app import db

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

def test_get_materia_using_filter_asc(client, app):
    data = [
        {"id": "1", "name": "Comet", "type": "magic", "element": "non-elemental"},
        {"id": "2", "name": "Barrier", "type": "magic", "element": None},
        {"id": "3", "name": "Time", "type": "magic", "element": "time"},
        {"id": "4", "name": "A_test_name", "type": "test_type", "element": "test_element"},
        {"id": "5", "name": "Z_test_name", "type": "test_type", "element": "test_element"},
    ]

    with app.app_context():
        for d in data:
            new_materia = MateriaModel(**d)
            db.session.add(new_materia)
        db.session.commit()

    response = client.get("/materia?sort=asc")
    assert response.status_code == 200
    json = response.get_json()
    first_materia = json[0]
    last_materia = json[len(json)-1]
    assert first_materia == data[3]
    assert last_materia == data[4]

def test_get_materia_using_filter_desc(client, app):
    data = [
        {"id": "1", "name": "Comet", "type": "magic", "element": "non-elemental"},
        {"id": "2", "name": "Barrier", "type": "magic", "element": None},
        {"id": "3", "name": "Time", "type": "magic", "element": "time"},
        {"id": "4", "name": "A_test_name", "type": "test_type", "element": "test_element"},
        {"id": "5", "name": "Z_test_name", "type": "test_type", "element": "test_element"},
    ]

    with app.app_context():
        for d in data:
            new_materia = MateriaModel(**d)
            db.session.add(new_materia)
        db.session.commit()

    response = client.get("/materia?sort=desc")
    assert response.status_code == 200
    json = response.get_json()
    first_materia = json[0]
    last_materia = json[len(json)-1]
    print (json)
    assert first_materia == data[4]
    assert last_materia == data[3]
