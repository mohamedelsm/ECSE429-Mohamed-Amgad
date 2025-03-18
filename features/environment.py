import requests

BASE_URL = "http://localhost:4567"

def before_scenario(context, scenario):
    print(f"\nStarting scenario: {scenario.name}")
    # Ensure we have a clean state for each scenario
    context.response = None
    context.todo = None
    context.project = None
    context.category = None

def after_scenario(context, scenario):
    print(f"\nFinished scenario: {scenario.name}")
    # Cleanup any resources created during the scenario
    if hasattr(context, 'todo') and context.todo and 'id' in context.todo:
        try:
            requests.delete(f"{BASE_URL}/todos/{context.todo['id']}")
        except Exception as e:
            print(f"Error deleting todo: {e}")
    
    if hasattr(context, 'project') and context.project and 'id' in context.project:
        try:
            requests.delete(f"{BASE_URL}/projects/{context.project['id']}")
        except Exception as e:
            print(f"Error deleting project: {e}")
            
    if hasattr(context, 'category') and context.category and 'id' in context.category:
        try:
            requests.delete(f"{BASE_URL}/categories/{context.category['id']}")
        except Exception as e:
            print(f"Error deleting category: {e}")