import requests
import pytest

BASE_URL = "http://localhost:4567"

@pytest.fixture
def sample_project():
    body = {"title": "TestProject", "description": "Temporary"}
    response = requests.post(f"{BASE_URL}/projects", json=body)
    project = response.json()
    yield project
    requests.delete(f"{BASE_URL}/projects/{project['id']}")

def test_get_projects(sample_project):
    response = requests.get(f"{BASE_URL}/projects")
    assert response.status_code == 200
    assert response.json() is not None
    assert sample_project in response.json()["projects"]

def test_get_projects_with_filtering(sample_project):
    response = requests.get(f"{BASE_URL}/projects?title=TestProject")
    assert response.status_code == 200
    assert response.json() is not None
    assert [project['title'] == "TestProject" for project in response.json()["projects"]]

def test_create_project():
    body = {"title": "Test", "description": "Temp"}
    response = requests.post(f"{BASE_URL}/projects", json=body)
    project_id = response.json()["id"]
    assert response.status_code == 201
    assert response.json() is not None
    assert response.json()["title"] == "Test"
    assert response.json()["description"] == "Temp"
    requests.delete(f"{BASE_URL}/projects/{response.json()['id']}")
