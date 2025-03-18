import requests
from behave import when, then

BASE_URL = "http://localhost:4567"

@when(u'the user deletes the project with id {project_id}')
def step_impl(context, project_id):
    response = requests.delete(f"{BASE_URL}/projects/{project_id}")
    context.response = response
    print(f"Delete project response status code: {context.response.status_code}")
    context.deleted_project_id = project_id

@then(u'the project with id {project_id} is deleted successfully')
def step_impl(context, project_id):
    assert 200 <= context.response.status_code < 300, f"Expected success status code, but got {context.response.status_code}"
    
    # Verify the project no longer exists by attempting to get it
    verify_response = requests.get(f"{BASE_URL}/projects/{project_id}")
    assert verify_response.status_code == 404, f"Expected 404 status code when getting deleted project, but got {verify_response.status_code}"


@then(u'the project with id {project_id} does not appear in the project list')
def step_impl(context, project_id):
    # Get all projects
    response = requests.get(f"{BASE_URL}/projects")
    assert 200 <= response.status_code < 300
    
    projects = response.json()["projects"]
    project_ids = [str(project["id"]) for project in projects]
    
    # Verify the deleted project ID is not in the list
    assert project_id not in project_ids, f"Project {project_id} still appears in the project list after deletion"

@when(u'the user tries to delete the project with id {non_existing_id}')
def step_impl(context, non_existing_id):
    response = requests.delete(f"{BASE_URL}/projects/{non_existing_id}")
    context.response = response
    print(f"Delete non-existent project response status code: {context.response.status_code}")

@given(u'that project with id {project_id} has been deleted')
def step_impl(context, project_id):
    context.deleted_project_id = project_id
    pass