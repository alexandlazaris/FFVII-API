import pytest
from app import create_app
from resources.characters import characters

def test_create_characters(client):
    response = client.post('/characters/data')
    assert response.status_code == 201
    print (response.get_json())

def test_get_characters(client):
    response = client.get('/characters')
    assert response.status_code == 200
    print (response.get_json())


