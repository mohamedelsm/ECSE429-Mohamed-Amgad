import requests
import pytest

BASE_URL = "http://localhost:4567"

@pytest.fixture(autouse=True, scope="session")
def check_api_running():
    try:
        requests.get(BASE_URL)
    except requests.ConnectionError:
        pytest.skip("API server is not running")
        
@pytest.fixture
def sample_project():
    project_body = {"title": "TestProject", "description": "Temporary"}
    project_response = requests.post(f"{BASE_URL}/projects", json=project_body)
    project = project_response.json()

    category_body = {"title": "TestCategory"}
    category_response = requests.post(f"{BASE_URL}/projects/{project['id']}/categories", json=category_body)
    category = category_response.json()

    task_body = {"title": "TestTask"}
    task_response = requests.post(f"{BASE_URL}/projects/{project['id']}/tasks", json=task_body)
    task = task_response.json()

    project = requests.get(f"{BASE_URL}/projects/{project['id']}").json()['projects'][0]

    yield project

    requests.delete(f"{BASE_URL}/projects/{project['id']}/categories/{category['id']}")
    requests.delete(f"{BASE_URL}/projects/{project['id']}")

def test_get_projects(sample_project):
    response = requests.get(f"{BASE_URL}/projects")
    assert response.status_code == 200
    assert response.json() is not None
    # check that the sample_project id is in the response
    assert sample_project['id'] in [project['id'] for project in response.json()["projects"]]

def test_get_project_with_id(sample_project):
    response = requests.get(f"{BASE_URL}/projects/{sample_project['id']}")
    assert response.status_code == 200
    assert response.json() is not None
    assert len(response.json()['projects']) == 1
    assert response.json()['projects'][0]['title'] == "TestProject"
    assert response.json()['projects'][0]['id'] == sample_project['id']

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

def test_create_duplicate_project():
    body = {"id": "1", "title": "Test", "description": "Temp"}
    response = requests.post(f"{BASE_URL}/projects", json=body)
    assert response.status_code == 400

def test_create_project_with_invalid_parameter():
    body = {"not_a_real_parameter": "blah blah", "title": "Test", "description": "Temp"}
    response = requests.post(f"{BASE_URL}/projects", json=body)
    assert response.status_code == 400

def test_create_project_with_no_body():
    response = requests.post(f"{BASE_URL}/projects")
    assert response.status_code == 201
    assert response.json() is not None
    assert response.json()["title"] == ""
    assert response.json()["description"] == ""

def test_head_projects():
    response = requests.head(f"{BASE_URL}/projects")
    assert response.status_code == 200
    assert 'Content-Type' in response.headers

def test_modify_fields_in_project(sample_project):
    body = {"title": "NewTitle", "description": "NewDescription"}
    response = requests.put(f"{BASE_URL}/projects/{sample_project['id']}", json=body)
    assert response.status_code == 200
    assert response.json() is not None
    assert response.json()["title"] == "NewTitle"
    assert response.json()["description"] == "NewDescription"

def test_delete_project(sample_project):
    response = requests.delete(f"{BASE_URL}/projects/{sample_project['id']}")
    assert response.status_code == 200
    get_response = requests.get(f"{BASE_URL}/projects/{sample_project['id']}")
    assert get_response.status_code == 404

def test_delete_non_existent_project():
    response = requests.delete(f"{BASE_URL}/projects/99999999")
    assert response.status_code == 404

def test_get_categories_of_project(sample_project):
    response = requests.get(f"{BASE_URL}/projects/{sample_project['id']}/categories")
    assert response.status_code == 200
    assert response.json() is not None
    assert len(response.json()["categories"]) == 1

def test_create_category_for_project(sample_project):
    body = {"title": "TestCategory2"}
    response = requests.post(f"{BASE_URL}/projects/{sample_project['id']}/categories", json=body)
    assert response.status_code == 201
    assert response.json()['title'] == "TestCategory2"

def test_delete_category(sample_project):
    category_to_delete = sample_project['categories'][0]['id']
    response = requests.delete(f"{BASE_URL}/projects/{sample_project['id']}/categories/{category_to_delete}")
    assert response.status_code == 200
    category_response = requests.get(f"{BASE_URL}/projects/{sample_project['id']}/categories")
    assert category_response.status_code == 200
    assert len(category_response.json()['categories']) == 0

def test_get_tasks_of_project(sample_project):
    response = requests.get(f"{BASE_URL}/projects/{sample_project['id']}/tasks")
    assert response.status_code == 200
    assert response.json() is not None
    assert len(response.json()["todos"]) == 1

def test_create_task_for_project(sample_project):
    body = {"title": "TestTask2"}
    response = requests.post(f"{BASE_URL}/projects/{sample_project['id']}/tasks", json=body)
    assert response.status_code == 201
    assert response.json()['title'] == "TestTask2"

def test_delete_task(sample_project):
    task_to_delete = sample_project['tasks'][0]['id']
    response = requests.delete(f"{BASE_URL}/projects/{sample_project['id']}/tasks/{task_to_delete}")
    assert response.status_code == 200
    task_response = requests.get(f"{BASE_URL}/projects/{sample_project['id']}/tasks")
    assert task_response.status_code == 200
    assert len(task_response.json()['todos']) == 0

# test options method for getting headers
def test_options_projects(sample_project):
    response = requests.options(f"{BASE_URL}/projects/{sample_project['id']}")
    assert response.status_code == 200
    assert 'Allow' in response.headers
    assert 'GET' in response.headers['Allow']
    assert 'POST' in response.headers['Allow']
    assert 'HEAD' in response.headers['Allow']
