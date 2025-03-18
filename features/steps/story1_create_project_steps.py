from behave import *
import requests
from setup import start_api, is_api_running, stop_api

BASE_URL = "http://localhost:4567/projects"


# Background Step: Start the server if it's not already running
@given('the server is running')
def step_impl(context):
    # Start the API if it's not running
    if not is_api_running():
        context.api_process = start_api()
    assert is_api_running(), "Server is not running"

# Scenario Outline: Create a new project (Normal Flow)
@when('a user creates a project with title {title}, description {description}, and active status {active}')
def step_impl(context, title, description, active):
    payload = {
        "title": title,
        "description": description,
        "active": active.lower() == 'true'
    }
    context.response = requests.post(BASE_URL, json=payload)

@then('the project with title {title} is created with the correct details')
def step_impl(context, title):
    response = requests.get(BASE_URL)
    projects = response.json()["projects"]
    created_project = next((p for p in projects if p["title"] == title), None)
    assert created_project is not None, f"Project with title '{title}' not found"
    assert created_project["title"] == title

@then('the user is notified of the successful creation')
def step_impl(context):
    assert context.response.status_code == 201, f"Expected status code 201, got {context.response.status_code}"

# Scenario Outline: Update an existing project (Alternative Flow)
@when('the user updates the project with new title {new_title}, description {new_description}, and active status {new_active}')
def step_impl(context, new_title, new_description, new_active):
    project_id = context.response.json()['projects'][0]["id"]
    payload = {
        "title": new_title,
        "description": new_description,
        "active": new_active.lower() == 'true'
    }
    context.response = requests.put(f"{BASE_URL}/{project_id}", json=payload)

@then('the project with new title {new_title} is updated with the correct details')
def step_impl(context, new_title):
    response = requests.get(BASE_URL)
    updated_project = next((p for p in response.json()["projects"] if p["title"] == new_title), None)
    assert updated_project is not None, f"Project with title '{new_title}' not found"

@then('the user is notified of the successful update')
def step_impl(context):
    assert context.response.status_code == 200, f"Expected status code 200, got {context.response.status_code}"

# Scenario Outline: Create a project with an existing ID (Error Flow)
@given('a project with id {existing_id} already exists')
def step_impl(context, existing_id):
    context.response = requests.get(f"{BASE_URL}/{existing_id}")
    assert context.response.status_code == 200, f"Project with id '{existing_id}' does not exist"

@when('the user tries to create a new project with id {existing_id}, title {title}, description {description}, and active status {active}')
def step_impl(context, existing_id, title, description, active):
    payload = {
        "id": existing_id,
        "title": title,
        "description": description,
        "active": active.lower() == 'true'
    }
    context.response = requests.post(BASE_URL, json=payload)

@then('the user is notified of the error')
def step_impl(context):
    assert context.response.status_code == 400, f"Expected status code 400, got {context.response.status_code}"


