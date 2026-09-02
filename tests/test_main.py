import pytest
from fastapi.testclient import TestClient

from main import app, reset_store


@pytest.fixture(autouse=True)
def clear_tasks() -> None:
    reset_store()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_root(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Student Task API is running"


def test_create_and_get_task(client: TestClient) -> None:
    payload = {
        "title": "Finish homework",
        "description": "Complete math exercises",
        "student_name": "Alex",
    }
    create_response = client.post("/tasks", json=payload)
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["id"] == 1
    assert created["title"] == "Finish homework"
    assert created["student_name"] == "Alex"
    assert created["completed"] is False

    get_response = client.get("/tasks/1")
    assert get_response.status_code == 200
    assert get_response.json() == created


def test_list_tasks(client: TestClient) -> None:
    client.post(
        "/tasks",
        json={"title": "Task A", "student_name": "Sam"},
    )
    client.post(
        "/tasks",
        json={"title": "Task B", "student_name": "Jordan"},
    )
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task A"
    assert data[1]["title"] == "Task B"


def test_update_task(client: TestClient) -> None:
    client.post(
        "/tasks",
        json={"title": "Draft essay", "student_name": "Riley"},
    )
    response = client.put("/tasks/1", json={"completed": True, "title": "Submit essay"})
    assert response.status_code == 200
    updated = response.json()
    assert updated["completed"] is True
    assert updated["title"] == "Submit essay"
    assert updated["student_name"] == "Riley"


def test_delete_task(client: TestClient) -> None:
    client.post(
        "/tasks",
        json={"title": "Read chapter 2", "student_name": "Casey"},
    )
    delete_response = client.delete("/tasks/1")
    assert delete_response.status_code == 204

    get_response = client.get("/tasks/1")
    assert get_response.status_code == 404
    assert get_response.json() == {"error": "Task not found", "status_code": 404}


def test_get_missing_task_returns_404(client: TestClient) -> None:
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"error": "Task not found", "status_code": 404}


def test_update_missing_task_returns_404(client: TestClient) -> None:
    response = client.put(
        "/tasks/999",
        json={"title": "Updated homework", "student_name": "Alex"},
    )
    assert response.status_code == 404
    assert response.json() == {"error": "Task not found", "status_code": 404}


def test_delete_missing_task_returns_404(client: TestClient) -> None:
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"error": "Task not found", "status_code": 404}


def test_create_task_rejects_empty_title(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "", "student_name": "Alex"},
    )
    assert response.status_code == 400
    assert response.json() == {"error": "Title must not be empty", "status_code": 400}
