def test_check_health(client, app):
    response = client.get("/healthcheck")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "active"