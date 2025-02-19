import unittest
import requests
import xml.etree.ElementTree as ET

class TestTodosBase(unittest.TestCase):
    """Base class with setup and teardown for todos tests"""
    
    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://localhost:4567"
        # Verify API is running
        try:
            requests.get(cls.base_url)
        except requests.ConnectionError:
            raise unittest.SkipTest("API server is not running")

    def setUp(self):
        # Create a test todo for each test
        self.todo_data = {
            "title": "Test Todo",
            "description": "Test Description",
            "doneStatus": False
        }
        response = requests.post(f"{self.base_url}/todos", json=self.todo_data)
        self.test_todo = response.json()
        self.todo_id = self.test_todo.get('id')

    def tearDown(self):
        # Clean up by deleting test todo
        if hasattr(self, 'todo_id'):
            requests.delete(f"{self.base_url}/todos/{self.todo_id}")

class TestTodosGet(TestTodosBase):
    """Test GET operations for todos"""

    def test_get_all_todos(self):
        """Test getting all todos"""
        response = requests.get(f"{self.base_url}/todos")
        self.assertEqual(response.status_code, 200)
        todos = response.json()
        self.assertIsInstance(todos['todos'], list)
        
    def test_get_todos_xml(self):
        """Test getting todos in XML format"""
        headers = {'Accept': 'application/xml'}
        response = requests.get(f"{self.base_url}/todos", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/xml', response.headers['Content-Type'])
        # Verify XML can be parsed
        try:
            ET.fromstring(response.content)
        except ET.ParseError:
            self.fail("Response is not valid XML")

    def test_get_specific_todo(self):
        """Test getting a specific todo by ID"""
        response = requests.get(f"{self.base_url}/todos/{self.todo_id}")
        self.assertEqual(response.status_code, 200)
        todo = response.json()['todos'][0]
        self.assertEqual(todo['title'], self.todo_data['title'])

    def test_get_nonexistent_todo(self):
        """Test getting a todo with non-existent ID"""
        response = requests.get(f"{self.base_url}/todos/999999")
        self.assertEqual(response.status_code, 404)

    def test_get_todo_by_title(self):
        """Test getting todos filtered by title"""
        response = requests.get(f"{self.base_url}/todos?title={self.todo_data['title']}")
        self.assertEqual(response.status_code, 200)
        todos = response.json()['todos']
        self.assertTrue(any(todo['title'] == self.todo_data['title'] for todo in todos))

class TestTodosPost(TestTodosBase):
    """Test POST operations for todos"""

    def test_create_minimal_todo(self):
        """Test creating a todo with only required fields"""
        minimal_todo = {"title": "Minimal Todo"}
        response = requests.post(f"{self.base_url}/todos", json=minimal_todo)
        self.assertEqual(response.status_code, 201)
        created_todo = response.json()
        self.assertEqual(created_todo['title'], minimal_todo['title'])
        # Cleanup
        requests.delete(f"{self.base_url}/todos/{created_todo['id']}")

    def test_create_todo_xml(self):
        """Test creating a todo using XML"""
        headers = {
            'Content-Type': 'application/xml',
            'Accept': 'application/xml'
        }
        xml_data = """
        <todo>
            <title>XML Todo</title>
            <description>Created via XML</description>
            <doneStatus>false</doneStatus>
        </todo>
        """
        response = requests.post(f"{self.base_url}/todos", headers=headers, data=xml_data)
        self.assertEqual(response.status_code, 201)
        # Verify response is XML
        self.assertIn('application/xml', response.headers['Content-Type'])
        # Cleanup - need to parse ID from XML response
        todo_xml = ET.fromstring(response.content)
        todo_id = todo_xml.find('id').text
        requests.delete(f"{self.base_url}/todos/{todo_id}")

    def test_create_todo_missing_title(self):
        """Test creating a todo without required title field"""
        invalid_todo = {"description": "No Title"}
        response = requests.post(f"{self.base_url}/todos", json=invalid_todo)
        self.assertEqual(response.status_code, 400)

def test_create_todo_with_id(self):
    """Test creating a todo with ID (should not be allowed)"""
    todo_with_id = {
        "id": "123",
        "title": "Todo With ID"
    }
    response = requests.post(f"{self.base_url}/todos", json=todo_with_id)
    self.assertEqual(response.status_code, 201)  # Should still create successfully
    
    # Parse response carefully
    created_todo = response.json()
    if 'todos' in created_todo:
        created_todo = created_todo['todos'][0]  # Handle if response is wrapped in 'todos' array
    
    # Verify the ID is different (system should ignore provided ID)
    self.assertNotEqual(str(created_todo.get('id', '')), "123")
    
    # Cleanup
    if 'id' in created_todo:
        requests.delete(f"{self.base_url}/todos/{created_todo['id']}") 

class TestTodosPut(TestTodosBase):
    """Test PUT operations for todos"""

    def test_update_todo_full(self):
        """Test updating all fields of a todo"""
        updated_data = {
            "title": "Updated Todo",
            "description": "Updated Description",
            "doneStatus": True
        }
        response = requests.put(f"{self.base_url}/todos/{self.todo_id}", json=updated_data)
        self.assertEqual(response.status_code, 200)
        updated_todo = response.json()
        self.assertEqual(updated_todo['title'], updated_data['title'])
        self.assertEqual(updated_todo['description'], updated_data['description'])
        self.assertEqual(str(updated_todo['doneStatus']).lower(), str(updated_data['doneStatus']).lower())

    def test_update_nonexistent_todo(self):
        """Test updating a non-existent todo"""
        response = requests.put(
            f"{self.base_url}/todos/999999",
            json={"title": "Update Nonexistent"}
        )
        self.assertEqual(response.status_code, 404)

    def test_update_todo_xml(self):
        """Test updating a todo using XML"""
        headers = {
            'Content-Type': 'application/xml',
            'Accept': 'application/xml'
        }
        xml_data = f"""
        <todo>
            <title>Updated XML Todo</title>
            <description>Updated via XML</description>
            <doneStatus>true</doneStatus>
        </todo>
        """
        response = requests.put(
            f"{self.base_url}/todos/{self.todo_id}",
            headers=headers,
            data=xml_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/xml', response.headers['Content-Type'])

class TestTodosDelete(TestTodosBase):
    """Test DELETE operations for todos"""

    def test_delete_todo(self):
        """Test deleting a todo"""
        # Create a todo specifically for deletion
        create_response = requests.post(
            f"{self.base_url}/todos",
            json={"title": "Todo to Delete"}
        )
        todo_id = create_response.json()['id']
        
        # Delete the todo
        delete_response = requests.delete(f"{self.base_url}/todos/{todo_id}")
        self.assertEqual(delete_response.status_code, 200)
        
        # Verify todo is deleted
        get_response = requests.get(f"{self.base_url}/todos/{todo_id}")
        self.assertEqual(get_response.status_code, 404)

    def test_delete_nonexistent_todo(self):
        """Test deleting a non-existent todo"""
        response = requests.delete(f"{self.base_url}/todos/999999")
        self.assertEqual(response.status_code, 404)

    def test_delete_already_deleted_todo(self):
        """Test deleting an already deleted todo"""
        # Create and delete a todo
        create_response = requests.post(
            f"{self.base_url}/todos",
            json={"title": "Todo to Delete Twice"}
        )
        todo_id = create_response.json()['id']
        requests.delete(f"{self.base_url}/todos/{todo_id}")
        
        # Try to delete again
        second_delete = requests.delete(f"{self.base_url}/todos/{todo_id}")
        self.assertEqual(second_delete.status_code, 404)

class TestTodosCategories(TestTodosBase):
    """Test todo-category relationship operations"""

    def setUp(self):
        super().setUp()
        # Create a test category
        self.category_data = {"title": "Test Category"}
        response = requests.post(f"{self.base_url}/categories", json=self.category_data)
        self.category = response.json()
        self.category_id = self.category['id']

    def tearDown(self):
        # Clean up category
        if hasattr(self, 'category_id'):
            requests.delete(f"{self.base_url}/categories/{self.category_id}")
        super().tearDown()

    def test_add_category_to_todo(self):
        """Test adding a category to a todo"""
        response = requests.post(
            f"{self.base_url}/todos/{self.todo_id}/categories",
            json={"id": self.category_id}
        )
        self.assertEqual(response.status_code, 201)

    def test_get_todo_categories(self):
        """Test getting categories for a todo"""
        # First add a category
        requests.post(
            f"{self.base_url}/todos/{self.todo_id}/categories",
            json={"id": self.category_id}
        )
        
        # Then get categories
        response = requests.get(f"{self.base_url}/todos/{self.todo_id}/categories")
        self.assertEqual(response.status_code, 200)
        categories = response.json()
        self.assertTrue(any(cat['id'] == self.category_id for cat in categories['categories']))

    def test_remove_category_from_todo(self):
        """Test removing a category from a todo"""
        # First add a category
        requests.post(
            f"{self.base_url}/todos/{self.todo_id}/categories",
            json={"id": self.category_id}
        )
        
        # Then remove it
        response = requests.delete(
            f"{self.base_url}/todos/{self.todo_id}/categories/{self.category_id}"
        )
        self.assertEqual(response.status_code, 200)

class TestTodosTasksOf(TestTodosBase):
    """Test todo-project relationship operations"""

    def setUp(self):
        super().setUp()
        # Create a test project
        self.project_data = {"title": "Test Project"}
        response = requests.post(f"{self.base_url}/projects", json=self.project_data)
        self.project = response.json()
        self.project_id = self.project['id']

    def tearDown(self):
        # Clean up project
        if hasattr(self, 'project_id'):
            requests.delete(f"{self.base_url}/projects/{self.project_id}")
        super().tearDown()

    def test_add_todo_to_project(self):
        """Test adding a todo to a project"""
        response = requests.post(
            f"{self.base_url}/todos/{self.todo_id}/tasksof",
            json={"id": self.project_id}
        )
        self.assertEqual(response.status_code, 201)

    def test_get_todo_projects(self):
        """Test getting projects for a todo"""
        # First add to project
        requests.post(
            f"{self.base_url}/todos/{self.todo_id}/tasksof",
            json={"id": self.project_id}
        )
        
        # Then get projects
        response = requests.get(f"{self.base_url}/todos/{self.todo_id}/tasksof")
        self.assertEqual(response.status_code, 200)
        projects = response.json()
        self.assertTrue(any(proj['id'] == self.project_id for proj in projects['projects']))

    def test_remove_todo_from_project(self):
        """Test removing a todo from a project"""
        # First add to project
        requests.post(
            f"{self.base_url}/todos/{self.todo_id}/tasksof",
            json={"id": self.project_id}
        )
        
        # Then remove it
        response = requests.delete(
            f"{self.base_url}/todos/{self.todo_id}/tasksof/{self.project_id}"
        )
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main() 