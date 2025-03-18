from behave import when, then
import requests

BASE_URL = "http://localhost:4567"

def step_impl(context, title):
    payload = {"title": title}
    response = requests.post(f"{BASE_URL}/projects", json=payload)
    assert response.status_code == 201
    context.project = response.json()

@when('the user adds the todo to the project')
def step_impl(context):
    context.response = requests.post(
        f"{BASE_URL}/todos/{context.todo['id']}/tasksof",
        json={"id": context.project['id']}
    )

@then('the todo is successfully associated with the project')
def step_impl(context):
    assert context.response.status_code == 201

@then('the project\'s tasks include the todo')
def step_impl(context):
    response = requests.get(f"{BASE_URL}/projects/{context.project['id']}/tasks")
    tasks = response.json()["todos"]
    assert any(task["id"] == context.todo["id"] for task in tasks)

@when('the user requests the project\'s tasks')
def step_impl(context):
    context.response = requests.get(f"{BASE_URL}/projects/{context.project['id']}/tasks")

@then('the response includes the todo')
def step_impl(context):
    assert context.response.status_code == 200
    tasks = context.response.json()["todos"]
    assert any(task["id"] == context.todo["id"] for task in tasks)

@when('the user tries to add the todo to a project with id {invalid_id}')
def step_impl(context, invalid_id):
    context.response = requests.post(
        f"{BASE_URL}/todos/{context.todo['id']}/tasksof",
        json={"id": invalid_id.strip('"')}
    )
