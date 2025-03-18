import requests
from behave import when, then

BASE_URL = "http://localhost:4567"

@when('the user requests the list of projects')
def step_when_request_list_projects(context):
    response = requests.get(f"{BASE_URL}/projects")
    context.response = response
    print(f"List projects response status code: {context.response.status_code}")
    context.project_list = response.json()["projects"] if 200 <= response.status_code < 300 else []

@when('the user filters the projects by active status {status}')
def step_when_filter_projects_by_status(context, status):
    # Construct the query parameter
    query_params = {"active": status}
    
    response = requests.get(f"{BASE_URL}/projects", params=query_params)
    context.response = response
    context.filtered_projects = response.json()["projects"] if 200 <= response.status_code < 300 else []

@then('all projects are displayed')
def step_then_all_projects_displayed(context):
    assert 200 <= context.response.status_code < 300, f"Expected success status code, but got {context.response.status_code}"
    assert len(context.project_list) > 0, "Expected at least one project to be displayed"

@then('only projects with the active status {status} are displayed')
def step_then_projects_filtered_by_status(context, status):
    assert 200 <= context.response.status_code < 300, f"Expected success status code, but got {context.response.status_code}"
    
    is_active = status.lower() == "true"
    
    # Check that all returned projects have the correct active status
    for project in context.filtered_projects:
        project_active = str(project.get("active", "false")).lower() == "true"
        assert project_active == is_active, f"Project {project['id']} has active={project.get('active')}, expected {clean_status}"

@then('the user receives an empty list')
def step_then_empty_list_received(context):
    assert 200 <= context.response.status_code < 300, f"Expected success status code, but got {context.response.status_code}"
    assert context.filtered_projects == [], "Expected an empty list of projects"