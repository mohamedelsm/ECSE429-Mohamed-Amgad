from behave import given, when, then
import requests
import re

BASE_URL = "http://localhost:4567"

def step_impl(context, title):
    payload = {"title": title}
    response = requests.post(f"{BASE_URL}/categories", json=payload)
    assert response.status_code == 201
    context.category = response.json()

@when('the user adds the category to the todo')
def step_impl(context):
    context.response = requests.post(
        f"{BASE_URL}/todos/{context.todo['id']}/categories",
        json={"id": context.category['id']}
    )

@then('the category is successfully associated with the todo')
def step_impl(context):
    assert context.response.status_code == 201

@then('the todo\'s categories include "{category_title}"')
def step_impl(context, category_title):
    response = requests.get(f"{BASE_URL}/todos/{context.todo['id']}/categories")
    categories = response.json()["categories"]
    assert any(cat["title"] == category_title for cat in categories)

@when('the user requests the todo\'s categories')
def step_impl(context):
    context.response = requests.get(f"{BASE_URL}/todos/{context.todo['id']}/categories")

@then('the response includes the category "{category_title}"')
def step_impl(context, category_title):
    assert context.response.status_code == 200
    categories = context.response.json()["categories"]
    assert any(cat["title"] == category_title for cat in categories)

@when('the user tries to add a category with id {invalid_id} to the todo')
def step_impl(context, invalid_id):
    context.response = requests.post(
        f"{BASE_URL}/todos/{context.todo['id']}/categories",
        json={"id": invalid_id.strip('"')}
    )

@given(re.compile(r'^a category with title "(?P<title>[^"]+)" exists$'))
def step_impl_category(context, title):
    payload = {"title": title}
    response = requests.post(f"{BASE_URL}/categories", json=payload)
    assert response.status_code == 201, f"Category creation failed: {response.status_code}"
    context.category = response.json()

@given('a category with title "Test Category" exists')
def step_impl_test_category(context):
    step_impl_category(context, "Test Category")

@given('a category with title "Office Tasks" exists')
def step_impl_office_tasks_category(context):
    step_impl_category(context, "Office Tasks")

@given('a category with title "Personal Errands" exists')
def step_impl_personal_errands_category(context):
    step_impl_category(context, "Personal Errands")

@given('a category with title "Development" exists')
def step_impl_development_category(context):
    step_impl_category(context, "Development")

@given('a category with title "Meetings" exists')
def step_impl_meetings_category(context):
    step_impl_category(context, "Meetings")

@given('a category with title "Team Activities" exists')
def step_impl_team_activities_category(context):
    step_impl_category(context, "Team Activities")

@given('a category with title "Development Tasks" exists')
def step_impl_development_tasks_category(context):
    step_impl_category(context, "Development Tasks")

@given('a category with title "Health" exists')
def step_impl_health_category(context):
    step_impl_category(context, "Health")

@given('a category with title "Social Events" exists')
def step_impl_social_events_category(context):
    step_impl_category(context, "Social Events")