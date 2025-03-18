import requests
from behave import given, when, then

BASE_URL = "http://localhost:4567/projects"

@given('a project with id {project_id} already exists')
def step_given_project_exists(context, project_id):
    response = requests.get(f"{BASE_URL}/{project_id}")
    context.response = response
    assert response.status_code == 200, f"Expected project with id {project_id} to exist, but it does not."

@given('no project with id {project_id} exists')
def step_given_no_project_exists(context, project_id):
    response = requests.get(f"{BASE_URL}/{project_id}")
    context.response = response
    assert response.status_code == 404, f"Expected project with id {project_id} to not exist, but it does."

@then('the user is notified of the success')
def step_then_user_notified_success(context):
    assert 200 <= context.response.status_code < 300, "Expected success response, but got an error."

@then('the user is notified of the error')
def step_then_user_notified_error(context):
    assert context.response.status_code >= 400, "Expected error response, but got success."