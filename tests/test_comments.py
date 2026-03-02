from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_comment():
    response = client.post(
        "/comments",
        json={"text": "Test comment", "category": "positive"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "Test comment"
    assert data["category"] == "positive"


def test_newest_on_top():
    client.post("/comments", json={"text": "Old", "category": "positive"})
    client.post("/comments", json={"text": "New", "category": "positive"})

    response = client.get("/comments")
    data = response.json()

    assert data["items"][0]["text"] == "New"


def test_pagination():
    for i in range(5):
        client.post("/comments", json={"text": f"Item {i}", "category": "positive"})

    response = client.get("/comments?page=1&limit=2")
    data = response.json()

    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["limit"] == 2


def test_filter_by_category():
    client.post("/comments", json={"text": "Positive one", "category": "positive"})
    client.post("/comments", json={"text": "Negative one", "category": "negative"})

    response = client.get("/comments?category=negative")
    data = response.json()

    for item in data["items"]:
        assert item["category"] == "negative"