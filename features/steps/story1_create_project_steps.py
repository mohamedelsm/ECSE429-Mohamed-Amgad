import requests

BASE_URL = "http://localhost:4567/projects"

from behave import when, then

@when('a user creates a project with title {title}, description {description}, and active status {active}')
def step_when_create_project_with_details(context, title, description, active):
    payload = {
        "title": title,
        "description": description,
        "active": active.lower() == "true"  # Convert string to boolean
    }
    response = requests.post(f"{BASE_URL}", json=payload)
    context.response = response
    print(context.response.status_code)
    context.created_project = response.json() if response.status_code == 201 else None

@when('the user creates a project with the title {title}')
def step_when_create_project_with_title(context, title):
    payload = {
        "title": title
    }
    response = requests.post(f"{BASE_URL}", json=payload)
    context.response = response
    context.created_project = response.json() if response.status_code == 201 else None

@when('the user tries to create a new project with id {project_id}, title {title}, description {description}, and active status {active}')
def step_when_create_project_with_id(context, project_id, title, description, active):
    payload = {
        "id": int(project_id),  # Convert project_id to integer
        "title": title,
        "description": description,
        "active": active.lower() == "true"  # Convert string to boolean
    }
    response = requests.post(f"{BASE_URL}/projects", json=payload)
    context.response = response

@then('the project with title {title} is created with the correct details')
def step_then_project_created_with_details(context, title):
    assert context.response.status_code == 201, f"Expected status code 201, but got {context.response.status_code}"
    assert context.created_project["title"] == title
    assert "description" in context.created_project
    assert "active" in context.created_project

@then('the project is created with the title {title} and default values for description and active status')
def step_then_project_created_with_defaults(context, title):
    assert context.response.status_code == 201, f"Expected status code 201, but got {context.response.status_code}"
    assert context.created_project["title"] == title
    assert context.created_project["description"] == ""
    assert context.created_project["active"] == "false"