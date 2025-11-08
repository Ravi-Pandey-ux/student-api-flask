import pytest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from run import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_add_student(client):
    response = client.post("/students", json={
        "id": "101",
        "name": "Ravi",
        "grade": "A",
        "subjects": ["Math", "Science"]
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "Student added"

def test_get_students(client):
    response = client.get("/students")
    assert response.status_code == 200
    students = response.get_json()
    assert isinstance(students, list)
    assert any(s["id"] == "101" for s in students)

def test_delete_student(client):
    response = client.delete("/students/101")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Student deleted"

def test_delete_nonexistent_student(client):
    response = client.delete("/students/999")
    assert response.status_code == 404
    assert "not found" in response.get_json()["error"]

def test_duplicate_student(client):
    client.post("/students", json={
        "id": "102",
        "name": "Ravi",
        "grade": "A",
        "subjects": ["Math"]
    })
    response = client.post("/students", json={
        "id": "102",
        "name": "Ravi",
        "grade": "A",
        "subjects": ["Math"]
    })
    assert response.status_code == 400
    assert "already exists" in response.get_json()["error"]

def test_update_student(client):
    # First add a student
    client.post("/students", json={
        "id": "201",
        "name": "Ravi",
        "grade": "B",
        "subjects": ["Math"]
    })

    # Update the student
    response = client.put("/students/201", json={
        "name": "Ravi Updated",
        "grade": "A",
        "subjects": ["Math", "Science"]
    })
    assert response.status_code == 200   # ✅ success
    assert response.get_json()["message"] == "Student updated"

def test_update_nonexistent_student(client):
    response = client.put("/students/999", json={
        "name": "Ghost",
        "grade": "C",
        "subjects": ["History"]
    })
    assert response.status_code == 404   # ✅ not found
    assert "not found" in response.get_json()["error"]


