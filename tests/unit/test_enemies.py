def test_create_enemies(client):
    response = client.post("/enemies/data")
    assert response.status_code == 201


def test_update_enemy_data(client):
    body = {
        "description": "unit test",
        "disc": "unit test",
        "hp": 10000,
        "location": "unit test",
        "name": "unit test",
        "steal": "unit test",
    }
    # arrange
    client.post("/enemies/data")

    # act, assert
    response = client.put("/enemies/1", json=body)
    data = response.get_json()
    assert response.status_code == 200
    assert data["description"] == "unit test"
    assert data["disc"] == "unit test"
    assert data["hp"] == 10000
    assert data["location"] == "unit test"
    assert data["name"] == "unit test"
    assert data["steal"] == "unit test"
