import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test 1: Home route returns 200
def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"running" in response.data

# Test 2: Get all students
def test_get_students(client):
    response = client.get('/students')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2

# Test 3: Get a valid student by ID
def test_get_student_valid(client):
    response = client.get('/students/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Alice"

# Test 4: Get invalid student (404 check)
def test_get_student_invalid(client):
    response = client.get('/students/999')
    assert response.status_code == 404
    assert b"not found" in response.data

# Test 5: Add a new student
def test_add_student(client):
    payload = {"name": "Charlie", "grade": "A+"}
    response = client.post('/students', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Charlie"

# Test 6: Add student with missing data (400 check)
def test_add_student_invalid(client):
    response = client.post('/students', json={"name": "Incomplete"})
    assert response.status_code == 400