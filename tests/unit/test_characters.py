def test_create_characters(client):
    response = client.post('/characters/data')
    assert response.status_code == 201

def test_get_characters(client):
    response = client.get('/characters')
    assert response.status_code == 200