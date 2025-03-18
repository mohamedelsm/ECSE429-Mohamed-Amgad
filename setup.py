import subprocess
import time
import requests

JAR_FILE = "runTodoManagerRestAPI-1.5.5.jar"
API_URL = "http://localhost:4567"

def start_api():
    """Starts the REST API server."""
    try:
        print("Starting the REST API...")
        process = subprocess.Popen(["java", "-jar", JAR_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)  # Wait for API to initialize
        return process
    except Exception as e:
        print(f"Error starting API: {e}")
        return None

def is_api_running():
    """Checks if the REST API is running."""
    try:
        response = requests.get(API_URL)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

if __name__ == "__main__":
    api_process = start_api()

    if api_process and is_api_running():
        print("API is running successfully.")
    else:
        print("Failed to start API. Check logs for errors.")