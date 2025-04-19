def test_get_party(client):
    response = client.get("/party")
    assert response.status_code == 200


def test_create_party_of_3(client):
    body = [{"name": "Barret"}, {"name": "Cid"}, {"name": "Cait Sith"}]
    response = client.post(
        "/party", json=body
    )
    assert response.status_code == 201
