def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["service"] == "mcp-djen-server"


def test_courts_returns_four(client):
    response = client.get("/courts")
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_intimations_happy_path(client):
    response = client.get(
        "/intimations",
        params={
            "name": "PEDRO BRANDÃO",
            "date_start": "2025-08-06",
            "date_end": "2025-08-06",
        },
    )
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_invalid_date_returns_400(client):
    response = client.get(
        "/intimations",
        params={
            "name": "PEDRO BRANDÃO",
            "date_start": "invalid-date",
            "date_end": "2025-08-06",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid date format. Use YYYY-MM-DD"


def test_unknown_route_is_404(client):
    response = client.get("/no-such-route")
    assert response.status_code == 404
    body = response.json()
    assert body["error"] == "NOT_FOUND"
    assert body["message"] == "Endpoint not found"
