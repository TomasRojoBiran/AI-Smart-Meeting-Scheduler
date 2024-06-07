import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to AI Smart Meeting Scheduler" in response.data


def test_schedule(client):
    response = client.post("/schedule", json={"email": "Meeting request email content"})
    assert response.status_code == 200
    assert "scheduled_time" in response.get_json()
