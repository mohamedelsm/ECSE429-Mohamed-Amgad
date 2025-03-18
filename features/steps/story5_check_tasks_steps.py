import requests
from behave import when, then, given

BASE_URL = "http://localhost:4567"

@given('a task with id {task_id} is assigned to the project with id {project_id}')
def step_given_task_assigned_to_project(context, task_id, project_id):
    context.project_id = project_id
    context.task_id = task_id
    
    # Get all tasks for the project
    response = requests.get(f"{BASE_URL}/projects/{project_id}/tasks")
    context.response = response
    assert 200 <= response.status_code < 300, f"Failed to get tasks for project with ID {project_id}"

    #check if tasks is in the list of tasks
    todos = response.json().get("todos", [])
    task_ids = [todo["id"] for todo in todos]
    assert task_id in task_ids, f"Task with ID {task_id} is not assigned to project with ID {project_id}"
    

@when('the user checks the tasks assigned to the project with id {project_id}')
def step_when_check_tasks(context, project_id):
    response = requests.get(f"{BASE_URL}/projects/{project_id}/tasks")
    context.response = response
    context.tasks = response.json().get("todos", [])

@when('the user retrieves the task with id {task_id} from the project with id {project_id}')
def step_when_get_task_by_id(context, task_id, project_id):
    # Get the tasks for the project
    response = requests.get(f"{BASE_URL}/projects/{project_id}/tasks")
    context.response = response
    todos = response.json().get("todos", [])
    # Find the specific task by ID
    context.task = next((todo for todo in todos if todo["id"] == task_id), None)
    # Assert that the task was found
    assert context.task is not None, f"Task {task_id} not found in project {project_id}"
    print(f"Found task {task_id} in project {project_id}")

@then('a list of all tasks assigned to the project is displayed')
def step_then_tasks_displayed(context):
    assert 200 <= context.response.status_code < 300, f"Expected success status code, but got {context.response.status_code}"
    assert len(context.tasks) > 0, "Expected at least one task to be displayed"

@then('the task with the associated id is displayed')
def step_then_task_displayed(context):
    assert 200 <= context.response.status_code < 300, f"Expected success status code, but got {context.response.status_code}"
    assert context.task is not None, "Expected task to be displayed"
    assert str(context.task["id"]) == context.task_id, f"Expected task ID {context.task_id}, but got {context.task['id']}"

@when('the user tries to check the task with {nonexistent_task_id} assigned to the project with id {project_id}')
def step_when_check_nonexistent_task(context, nonexistent_task_id, project_id):
    response = requests.get(f"{BASE_URL}/projects/{project_id}/tasks/{nonexistent_task_id}")
    context.response = response
    