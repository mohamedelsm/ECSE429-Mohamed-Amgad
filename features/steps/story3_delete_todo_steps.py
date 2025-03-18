from behave import given, when, then
import requests
from setup import start_api, is_api_running

BASE_URL = "http://localhost:4567/todos"

@when('the user deletes the todo')
def step_impl(context):
    context.response = requests.delete(f"{BASE_URL}/{context.todo['id']}")

@then('the todo is successfully deleted')
def step_impl(context):
    assert context.response.status_code == 200
    # Verify the todo no longer exists
    get_response = requests.get(f"{BASE_URL}/{context.todo['id']}")
    assert get_response.status_code == 404

@then('subsequent retrieval of the todo returns not found')
def step_impl(context):
    get_response = requests.get(f"{BASE_URL}/{context.todo['id']}")
    assert get_response.status_code == 404

@then('the todo no longer appears in the list of all todos')
def step_impl(context):
    response = requests.get(BASE_URL)
    todos = response.json()["todos"]
    assert not any(t["id"] == context.todo["id"] for t in todos)

@when('the user attempts to delete the same todo again')
def step_impl(context):
    # Try to delete the already deleted todo
    context.response = requests.delete(f"{BASE_URL}/{context.todo['id']}")