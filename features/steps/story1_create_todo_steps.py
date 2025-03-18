from behave import when, then, given
import requests
import re
BASE_URL = "http://localhost:4567/todos"

@when('a user creates a todo with title {title} and description {description}')
def step_impl_create_todo(context, title, description):
    payload = {
        "title": title.strip('"'),
        "description": description.strip('"')
    }
    context.response = requests.post(BASE_URL, json=payload)

@when('a user creates a todo with only title {title}')
def step_impl_create_todo_only_title(context, title):
    payload = {"title": title.strip('"')}
    context.response = requests.post(BASE_URL, json=payload)

@when('a user tries to create a todo with description {description} but no title')
def step_impl_create_todo_no_title(context, description):
    payload = {"description": description.strip('"')}
    context.response = requests.post(BASE_URL, json=payload)

@then('the todo with title {title} is created with the correct details')
def step_impl_check_todo_created(context, title):
    response = requests.get(BASE_URL)
    todos = response.json()["todos"]
    created_todo = next((t for t in todos if t["title"] == title.strip('"')), None)
    assert created_todo is not None, f"Todo with title '{title}' not found"
    assert created_todo["title"] == title.strip('"')

@then('the todo has an empty description')
def step_impl_check_empty_description(context):
    todos = requests.get(BASE_URL).json()["todos"]
    created_todo = next((t for t in todos if t["id"] == context.response.json()["id"]), None)
    assert created_todo is not None, "Created todo not found"
    assert created_todo.get("description", "") == "", f"Expected empty description, got '{created_todo.get('description', '')}'"

