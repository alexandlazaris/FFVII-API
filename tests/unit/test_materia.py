def test_create_materia_data(client):
    response = client.post("/materia/data")
    assert response.status_code == 201


def test_create_new_materia(client):
    body = [{"name": "bolt", "element": "lightning", "level": 1}]
    response = client.post("/materia", json=body)
    assert response.status_code == 201


def test_get_all_materia(client):
    body = [
        {"name": "bolt", "element": "lightning", "level": 1},
        {"name": "bio", "element": "poison", "level": 2},
    ]
    client.post("/materia", json=body)

    response = client.get("/materia")
    assert response.status_code == 200
