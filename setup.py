import subprocess
import time
import requests
import os
import signal

JAR_FILE = "runTodoManagerRestAPI-1.5.5.jar"
API_URL = "http://localhost:4567"

def start_api():
    """Starts the REST API server and returns the process."""
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

def stop_api(process):
    """Stops the running API server."""
    if process:
        print("Stopping the REST API...")
        process.terminate()  # Terminate the API process
        process.wait()  # Wait for the process to terminate properly
        print("API stopped.")
    else:
        print("No running API process found.")