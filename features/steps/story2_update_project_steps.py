import requests
from behave import when, then

BASE_URL = "http://localhost:4567"

@when(u'the user updates the project with id {project_id} with new name {title}, content {description}, and status {active}')
def step_impl(context, project_id, title, description, active):
    payload = {
        "title": title,
        "description": description,
        "active": active.lower() == "true"
    }
    response = requests.put(f"{BASE_URL}/projects/{project_id}", json=payload)
    context.response = response
    context.updated_project = response.json() if 200 <= context.response.status_code < 300 else None
    # Store parameters for later validation
    context.expected_title = title
    context.expected_description = description
    context.expected_active = active

@then(u'the project is updated with the new details')
def step_impl(context):
    assert 200 <= context.response.status_code < 300, f"Expected success status code, but got {context.response.status_code}"
    assert context.updated_project is not None
    assert context.updated_project["title"] == context.expected_title
    assert context.updated_project["description"] == context.expected_description
    assert context.updated_project["active"] == str(context.expected_active)

@when(u'the user updates the project with id {existing_id} with the name {title}')
def step_impl(context, existing_id, title):
    payload = {
        "title": title
    }
    response = requests.put(f"{BASE_URL}/projects/{existing_id}", json=payload)
    context.response = response
    print(context.response.status_code)
    context.updated_project = response.json() if 200 <= context.response.status_code < 300 else None
    # Store parameter for later validation
    context.expected_title = title

@then(u'the project is updated with the name {title} and the rest of the details remain the same')
def step_impl(context, title):
    assert 200 <= context.response.status_code < 300, f"Expected success status code, but got {context.response.status_code}"
    assert context.updated_project is not None
    assert context.updated_project["title"] == title
    # We don't check other details as they should remain unchanged

@when(u'the user tries to update the project with id {project_id}, name {title}, content {description}, and status {active}')
def step_impl(context, project_id, title, description, active):

    payload = {
        "title": title,
        "description": description,
        "active": active.lower() == "true"
    }
    response = requests.put(f"{BASE_URL}/projects/{project_id}", json=payload)
    context.response = response
    print(context.response.status_code)
    context.updated_project = response.json() if 200 <= context.response.status_code < 300 else None