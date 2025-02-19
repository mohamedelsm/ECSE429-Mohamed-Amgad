import pytest
import requests
import xml.etree.ElementTree as ET

BASE_URL = "http://localhost:4567"

# Automatically check if the API is running for all tests in this session
@pytest.fixture(autouse=True, scope="session")
def check_api_running():
    try:
        requests.get(BASE_URL)
    except requests.ConnectionError:
        pytest.skip("API server is not running")

# Fixture to create and cleanup a sample todo for tests
@pytest.fixture
def sample_todo():
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description",
        "doneStatus": False
    }
    response = requests.post(f"{BASE_URL}/todos", json=todo_data)
    todo = response.json()
    yield todo
    requests.delete(f"{BASE_URL}/todos/{todo['id']}")

# Fixture for a sample category (used in todos-categories tests)
@pytest.fixture
def sample_category():
    category_data = {"title": "Test Category"}
    response = requests.post(f"{BASE_URL}/categories", json=category_data)
    category = response.json()
    yield category
    requests.delete(f"{BASE_URL}/categories/{category['id']}")

# Fixture for a sample project (used in todos-tasksof tests)
@pytest.fixture
def sample_project():
    project_data = {"title": "Test Project"}
    response = requests.post(f"{BASE_URL}/projects", json=project_data)
    project = response.json()
    yield project
    requests.delete(f"{BASE_URL}/projects/{project['id']}")

def test_get_all_todos(sample_todo):
    response = requests.get(f"{BASE_URL}/todos")
    assert response.status_code == 200
    todos = response.json()
    assert isinstance(todos['todos'], list)

def test_get_todos_xml(sample_todo):
    headers = {'Accept': 'application/xml'}
    response = requests.get(f"{BASE_URL}/todos", headers=headers)
    assert response.status_code == 200
    assert 'application/xml' in response.headers['Content-Type']
    try:
        ET.fromstring(response.content)
    except ET.ParseError:
        pytest.fail("Response is not valid XML")

def test_get_specific_todo(sample_todo):
    response = requests.get(f"{BASE_URL}/todos/{sample_todo['id']}")
    assert response.status_code == 200
    json_resp = response.json()
    # Handle if the response is wrapped in a "todos" list 
    todo = json_resp.get('todos', [json_resp])[0]
    assert todo['title'] == sample_todo['title']

def test_get_nonexistent_todo():
    response = requests.get(f"{BASE_URL}/todos/999999")
    assert response.status_code == 404

def test_get_todo_by_title(sample_todo):
    response = requests.get(f"{BASE_URL}/todos?title={sample_todo['title']}")
    assert response.status_code == 200
    todos = response.json()['todos']
    assert any(todo['title'] == sample_todo['title'] for todo in todos)

def test_create_minimal_todo():
    minimal_todo = {"title": "Minimal Todo"}
    response = requests.post(f"{BASE_URL}/todos", json=minimal_todo)
    assert response.status_code == 201
    created_todo = response.json()
    assert created_todo['title'] == minimal_todo['title']
    # Cleanup
    requests.delete(f"{BASE_URL}/todos/{created_todo['id']}")

def test_create_todo_xml():
    headers = {
        'Content-Type': 'application/xml',
        'Accept': 'application/xml'
    }
    xml_data = """
    <todo>
        <title>XML Todo</title>
        <description>Created via XML</description>
        <doneStatus>false</doneStatus>
    </todo>
    """
    response = requests.post(f"{BASE_URL}/todos", headers=headers, data=xml_data)
    assert response.status_code == 201
    assert 'application/xml' in response.headers['Content-Type']
    # Parse XML and cleanup using extracted ID
    todo_xml = ET.fromstring(response.content)
    todo_id_elem = todo_xml.find('id')
    assert todo_id_elem is not None
    todo_id = todo_id_elem.text
    requests.delete(f"{BASE_URL}/todos/{todo_id}")

def test_create_todo_missing_title():
    invalid_todo = {"description": "No Title"}
    response = requests.post(f"{BASE_URL}/todos", json=invalid_todo)
    assert response.status_code == 400

def test_create_todo_with_id():
    todo_with_id = {
        "id": "123",
        "title": "Todo With ID"
    }
    response = requests.post(f"{BASE_URL}/todos", json=todo_with_id)
    # API should reject todos with predefined IDs
    assert response.status_code == 400

def test_update_todo_full(sample_todo):
    updated_data = {
        "title": "Updated Todo",
        "description": "Updated Description",
        "doneStatus": True
    }
    response = requests.put(f"{BASE_URL}/todos/{sample_todo['id']}", json=updated_data)
    assert response.status_code == 200
    updated_todo = response.json()
    assert updated_todo['title'] == updated_data['title']
    assert updated_todo['description'] == updated_data['description']
    assert str(updated_todo['doneStatus']).lower() == str(updated_data['doneStatus']).lower()

def test_update_nonexistent_todo():
    response = requests.put(f"{BASE_URL}/todos/999999", json={"title": "Update Nonexistent"})
    assert response.status_code == 404

def test_update_todo_xml(sample_todo):
    headers = {
        'Content-Type': 'application/xml',
        'Accept': 'application/xml'
    }
    xml_data = """
    <todo>
        <title>Updated XML Todo</title>
        <description>Updated via XML</description>
        <doneStatus>true</doneStatus>
    </todo>
    """
    response = requests.put(f"{BASE_URL}/todos/{sample_todo['id']}", headers=headers, data=xml_data)
    assert response.status_code == 200
    assert 'application/xml' in response.headers['Content-Type']

def test_delete_todo():
    # Create a todo specifically for deletion
    create_resp = requests.post(f"{BASE_URL}/todos", json={"title": "Todo to Delete"})
    assert create_resp.status_code == 201
    todo = create_resp.json()
    todo_id = todo['id']
    delete_resp = requests.delete(f"{BASE_URL}/todos/{todo_id}")
    assert delete_resp.status_code == 200
    get_resp = requests.get(f"{BASE_URL}/todos/{todo_id}")
    assert get_resp.status_code == 404

def test_delete_nonexistent_todo():
    response = requests.delete(f"{BASE_URL}/todos/999999")
    assert response.status_code == 404

def test_delete_already_deleted_todo():
    create_resp = requests.post(f"{BASE_URL}/todos", json={"title": "Todo to Delete Twice"})
    todo_id = create_resp.json()['id']
    requests.delete(f"{BASE_URL}/todos/{todo_id}")
    second_delete = requests.delete(f"{BASE_URL}/todos/{todo_id}")
    assert second_delete.status_code == 404

def test_add_category_to_todo(sample_todo, sample_category):
    response = requests.post(
        f"{BASE_URL}/todos/{sample_todo['id']}/categories", 
        json={"id": sample_category['id']}
    )
    assert response.status_code == 201

def test_get_todo_categories(sample_todo, sample_category):
    add_resp = requests.post(
        f"{BASE_URL}/todos/{sample_todo['id']}/categories", 
        json={"id": sample_category['id']}
    )
    assert add_resp.status_code == 201
    response = requests.get(f"{BASE_URL}/todos/{sample_todo['id']}/categories")
    assert response.status_code == 200
    categories = response.json()
    found = any(cat['id'] == sample_category['id'] for cat in categories.get('categories', []))
    assert found

def test_remove_category_from_todo(sample_todo, sample_category):
    add_resp = requests.post(
        f"{BASE_URL}/todos/{sample_todo['id']}/categories", 
        json={"id": sample_category['id']}
    )
    assert add_resp.status_code == 201
    response = requests.delete(f"{BASE_URL}/todos/{sample_todo['id']}/categories/{sample_category['id']}")
    assert response.status_code == 200

def test_add_todo_to_project(sample_todo, sample_project):
    response = requests.post(
        f"{BASE_URL}/todos/{sample_todo['id']}/tasksof", 
        json={"id": sample_project['id']}
    )
    assert response.status_code == 201

def test_get_todo_projects(sample_todo, sample_project):
    add_resp = requests.post(
        f"{BASE_URL}/todos/{sample_todo['id']}/tasksof", 
        json={"id": sample_project['id']}
    )
    assert add_resp.status_code == 201
    response = requests.get(f"{BASE_URL}/todos/{sample_todo['id']}/tasksof")
    assert response.status_code == 200
    projects = response.json()
    found = any(proj['id'] == sample_project['id'] for proj in projects.get('projects', []))
    assert found

def test_remove_todo_from_project(sample_todo, sample_project):
    add_resp = requests.post(
        f"{BASE_URL}/todos/{sample_todo['id']}/tasksof", 
        json={"id": sample_project['id']}
    )
    assert add_resp.status_code == 201
    response = requests.delete(f"{BASE_URL}/todos/{sample_todo['id']}/tasksof/{sample_project['id']}")
    assert response.status_code == 200 