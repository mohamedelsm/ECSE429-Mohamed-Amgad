import requests

BASE_URL = "http://localhost:4567"  # Replace with your API URL

def test_projects():
    response = requests.get(f"{BASE_URL}/projects")
    assert response.status_code == 200
    assert response.json() != []