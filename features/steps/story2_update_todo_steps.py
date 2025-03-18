from behave import when, then
import requests
import xml.etree.ElementTree as ET

BASE_URL = "http://localhost:4567/todos"

@when('the user updates the todo with new title {new_title} and new description {new_description}')
def step_impl_update_todo(context, new_title, new_description):
    payload = {
        "title": new_title.strip('"'),
        "description": new_description.strip('"')
    }
    context.response = requests.put(f"{BASE_URL}/{context.todo['id']}", json=payload)

@then('the todo with new title {new_title} is updated with the correct details')
def step_impl_check_updated_todo(context, new_title):
    # Make sure the update was successful
    assert context.response.status_code in [200, 201], f"Update failed with status {context.response.status_code}"
    
    # The response might contain the updated todo directly
    updated_todo = None
    try:
        # Try to get the todo from the response
        updated_todo = context.response.json()
        if "todos" in updated_todo:
            updated_todo = updated_todo["todos"][0]
    except:
        # If that fails, fetch the todo
        response = requests.get(f"{BASE_URL}/{context.todo['id']}")
        assert response.status_code == 200, f"Failed to get todo: {response.status_code}"
        updated_todo = response.json()
        if "todos" in updated_todo:
            updated_todo = updated_todo["todos"][0]
    
    # Check if the title matches
    clean_title = new_title.strip('"')
    assert updated_todo["title"] == clean_title, f"Expected title '{clean_title}', got '{updated_todo.get('title', 'not found')}'"

@when('the user updates the todo using XML format with title {title} and description {description}')
def step_impl_update_todo_xml(context, title, description):
    headers = {
        'Content-Type': 'application/xml',
        'Accept': 'application/xml'
    }
    xml_data = f"""
    <todo>
        <title>{title.strip('"')}</title>
        <description>{description.strip('"')}</description>
    </todo>
    """
    context.response = requests.put(f"{BASE_URL}/{context.todo['id']}", 
                                  headers=headers, 
                                  data=xml_data)

@then('the todo with title {title} is updated with the correct details')
def step_impl_check_updated_todo_by_title(context, title):
    # First check if we have XML response
    if 'application/xml' in context.response.headers.get('Content-Type', ''):
        # Parse XML response
        try:
            root = ET.fromstring(context.response.content)
            todo_title = root.find('.//title').text
            clean_title = title.strip('"')
            assert todo_title == clean_title, f"Expected title '{clean_title}', got '{todo_title}'"
            return
        except Exception as e:
            print(f"Error parsing XML: {e}")
    
    # If not XML or parsing failed, fetch the todo directly
    response = requests.get(f"{BASE_URL}/{context.todo['id']}")
    assert response.status_code == 200, f"Failed to get todo: {response.status_code}"
    
    updated_todo = response.json()
    if "todos" in updated_todo:
        updated_todo = updated_todo["todos"][0]
    
    clean_title = title.strip('"')
    assert updated_todo["title"] == clean_title, f"Expected title '{clean_title}', got '{updated_todo.get('title', 'not found')}'"

@then('the response is in XML format')
def step_impl_check_xml_response(context):
    assert 'application/xml' in context.response.headers.get('Content-Type', ''), "Response is not in XML format"
    
    # Verify we can parse it as XML
    try:
        ET.fromstring(context.response.content)
    except ET.ParseError:
        assert False, "Response is not valid XML"

@when('the user tries to update a non-existent todo with id {invalid_id}')
def step_impl_update_nonexistent_todo(context, invalid_id):
    payload = {
        "title": "Invalid Update",
        "description": "Should fail"
    }
    # Clean the invalid_id by stripping any extraneous quotes
    clean_invalid_id = invalid_id.strip('"')
    context.response = requests.put(f"{BASE_URL}/{clean_invalid_id}", json=payload)