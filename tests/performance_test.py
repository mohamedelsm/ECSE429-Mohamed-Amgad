import threading
import time
import psutil
import statistics
import pandas as pd
import matplotlib.pyplot as plt
import requests
import random
import string
import os

BASE_URL = "http://localhost:4567"

def random_string(length=10):
    """Generate a random string for test data"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Todo operations
def create_todo():
    """Create a todo with random data"""
    payload = {
        "title": f"Performance Test {random_string()}",
        "description": f"Description {random_string(20)}",
        "doneStatus": random.choice([True, False])
    }
    response = requests.post(f"{BASE_URL}/todos", json=payload)
    return response.json() if response.status_code == 201 else None

def delete_todo(todo_id):
    """Delete a todo by ID"""
    response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
    return response.status_code == 200

def update_todo(todo_id):
    """Update a todo with random data"""
    payload = {
        "title": f"Updated {random_string()}",
        "description": f"Updated description {random_string(20)}",
        "doneStatus": random.choice([True, False])
    }
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=payload)
    return response.json() if response.status_code == 200 else None

# Project operations
def create_project():
    """Create a project with random data"""
    payload = {
        "title": f"Project {random_string()}",
        "description": f"Project Description {random_string(20)}",
        "active": random.choice([True, False])
    }
    response = requests.post(f"{BASE_URL}/projects", json=payload)
    return response.json() if response.status_code == 201 else None

def delete_project(project_id):
    """Delete a project by ID"""
    response = requests.delete(f"{BASE_URL}/projects/{project_id}")
    return response.status_code == 200

def update_project(project_id):
    """Update a project with random data"""
    payload = {
        "title": f"Updated Project {random_string()}",
        "description": f"Updated project description {random_string(20)}",
        "active": random.choice([True, False])
    }
    response = requests.put(f"{BASE_URL}/projects/{project_id}", json=payload)
    return response.json() if response.status_code == 200 else None

class ResourceMonitor:
    def __init__(self, sample_interval=0.1):
        self.samples = []
        self.running = False
        self.sample_interval = sample_interval
        self.monitor_thread = None
        
    def start_monitoring(self):
        """Start collecting resource usage samples in a background thread"""
        self.samples = []
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_resources)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop collecting samples and wait for thread to finish"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
        
    def _monitor_resources(self):
        """Background thread function to collect samples"""
        process = psutil.Process()
        while self.running:
            try:
                self.samples.append({
                    'timestamp': time.time(),
                    'cpu_percent': process.cpu_percent(),
                    'memory_mb': process.memory_info().rss / (1024 * 1024)
                })
            except Exception as e:
                print(f"Error sampling resources: {e}")
            time.sleep(self.sample_interval)
    
    def get_statistics(self):
        """Calculate statistics from collected samples"""
        if not self.samples:
            return {
                'cpu_avg': 0,
                'cpu_max': 0,
                'memory_avg': 0, 
                'memory_max': 0,
                'samples': 0
            }
            
        cpu_values = [s['cpu_percent'] for s in self.samples]
        memory_values = [s['memory_mb'] for s in self.samples]
        
        return {
            'cpu_avg': statistics.mean(cpu_values) if cpu_values else 0,
            'cpu_max': max(cpu_values) if cpu_values else 0,
            'memory_avg': statistics.mean(memory_values) if memory_values else 0,
            'memory_max': max(memory_values) if memory_values else 0,
            'samples': len(self.samples)
        }
    
    def get_dataframe(self):
        """Return samples as pandas DataFrame"""
        return pd.DataFrame(self.samples)


def run_experiment(object_type, operation, object_counts):
    """Run experiments with resource monitoring during execution"""
    results = []
    monitor = ResourceMonitor(sample_interval=0.1)  # Sample every 100ms
    
    for count in object_counts:
        # Create objects first if needed
        if operation != "create":
            items = []
            create_func = create_todo if object_type == "todo" else create_project
            for _ in range(count):
                item = create_func()
                if item:
                    items.append(item["id"])
        
        # Start monitoring
        monitor.start_monitoring()
        
        # Time the operation
        start_time = time.time()
        
        if operation == "create":
            create_func = create_todo if object_type == "todo" else create_project
            for _ in range(count):
                create_func()
        elif operation == "delete":
            delete_func = delete_todo if object_type == "todo" else delete_project
            for item_id in items:
                delete_func(item_id)
        elif operation == "update":
            update_func = update_todo if object_type == "todo" else update_project
            for item_id in items:
                update_func(item_id)
        
        duration = time.time() - start_time
         
        # Stop monitoring
        monitor.stop_monitoring()
        
        # Get resource usage statistics
        stats = monitor.get_statistics()
        
        results.append({
            "count": count,
            "time_seconds": duration,
            "avg_time_per_op": duration / count if count > 0 else 0,
            "cpu_avg_percent": stats['cpu_avg'],
            "cpu_max_percent": stats['cpu_max'],
            "memory_avg_mb": stats['memory_avg'],
            "memory_max_mb": stats['memory_max'],
            "samples": stats['samples'],
            "operations_per_second": count / duration if duration > 0 else 0
        })
        
        print(f"Completed {object_type} {operation} test with {count} objects in {duration:.2f} seconds")
        print(f"  CPU: avg={stats['cpu_avg']:.1f}%, max={stats['cpu_max']:.1f}%")
        print(f"  Memory: avg={stats['memory_avg']:.1f}MB, max={stats['memory_max']:.1f}MB")
        
        # Small delay to let system stabilize
        time.sleep(2)
    
    return results

def create_separate_figures(todo_results, project_results):
    """Create and save separate figures for each metric"""
    
    # Convert results to DataFrame
    todo_df = pd.DataFrame()
    for operation, results in todo_results.items():
        op_df = pd.DataFrame(results)
        op_df['operation'] = operation
        todo_df = pd.concat([todo_df, op_df], ignore_index=True)
    
    project_df = pd.DataFrame()
    for operation, results in project_results.items():
        op_df = pd.DataFrame(results)
        op_df['operation'] = operation
        project_df = pd.concat([project_df, op_df], ignore_index=True)
    
    # Figure 1: Transaction time vs number of "todo" objects
    plt.figure(figsize=(10, 6))
    for operation in todo_df['operation'].unique():
        op_df = todo_df[todo_df['operation'] == operation]
        plt.plot(op_df['count'], op_df['time_seconds'], marker='o', label=operation)
    plt.title('Figure 1. Transaction Time versus Number of "todo" Objects')
    plt.xlabel('Number of "todo" Objects')
    plt.ylabel('Transaction Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('tests/figures/figure1_todo_time.png')
    plt.close()
    
    # Figure 2: CPU usage vs number of "todo" objects
    plt.figure(figsize=(10, 6))
    for operation in todo_df['operation'].unique():
        op_df = todo_df[todo_df['operation'] == operation]
        plt.plot(op_df['count'], op_df['cpu_avg_percent'], marker='o', label=operation)
    plt.title('Figure 2. CPU Usage versus Number of "todo" Objects')
    plt.xlabel('Number of "todo" Objects')
    plt.ylabel('CPU Usage (%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('tests/figures/figure2_todo_cpu.png')
    plt.close()
    
    # Figure 3: Memory usage vs number of "todo" objects
    plt.figure(figsize=(10, 6))
    for operation in todo_df['operation'].unique():
        op_df = todo_df[todo_df['operation'] == operation]
        plt.plot(op_df['count'], op_df['memory_avg_mb'], marker='o', label=operation)
    plt.title('Figure 3. Memory Usage versus Number of "todo" Objects')
    plt.xlabel('Number of "todo" Objects')
    plt.ylabel('Memory Usage (MB)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('tests/figures/figure3_todo_memory.png')
    plt.close()
    
    # Figure 4: Transaction time vs number of "project" objects
    plt.figure(figsize=(10, 6))
    for operation in project_df['operation'].unique():
        op_df = project_df[project_df['operation'] == operation]
        plt.plot(op_df['count'], op_df['time_seconds'], marker='o', label=operation)
    plt.title('Figure 4. Transaction Time versus Number of "project" Objects')
    plt.xlabel('Number of "project" Objects')
    plt.ylabel('Transaction Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('tests/figures/figure4_project_time.png')
    plt.close()
    
    # Figure 5: CPU usage vs number of "project" objects
    plt.figure(figsize=(10, 6))
    for operation in project_df['operation'].unique():
        op_df = project_df[project_df['operation'] == operation]
        plt.plot(op_df['count'], op_df['cpu_avg_percent'], marker='o', label=operation)
    plt.title('Figure 5. CPU Usage versus Number of "project" Objects')
    plt.xlabel('Number of "project" Objects')
    plt.ylabel('CPU Usage (%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('tests/figures/figure5_project_cpu.png')
    plt.close()
    
    # Figure 6: Memory usage vs number of "project" objects
    plt.figure(figsize=(10, 6))
    for operation in project_df['operation'].unique():
        op_df = project_df[project_df['operation'] == operation]
        plt.plot(op_df['count'], op_df['memory_avg_mb'], marker='o', label=operation)
    plt.title('Figure 6. Memory Usage versus Number of "project" Objects')
    plt.xlabel('Number of "project" Objects')
    plt.ylabel('Memory Usage (MB)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('tests/figures/figure6_project_memory.png')
    plt.close()
    
    print("Figures saved to tests/figures/ directory")
    
    # Save detailed results to CSV
    todo_df.to_csv('tests/todo_performance_results.csv', index=False)
    project_df.to_csv('tests/project_performance_results.csv', index=False)
    print("Results saved to CSV files")

if __name__ == "__main__":
    # Define the object counts to test with
    object_counts = [10, 50, 100, 200, 500, 1000]
    
    # Run experiments for todo operations (create, update, delete)
    todo_results = {}
    operations = ["create", "update", "delete"]
    
    for operation in operations:
        print(f"\nRunning TODO {operation.upper()} performance tests...")
        todo_results[operation] = run_experiment("todo", operation, object_counts)
    
    # Run experiments for project operations (create, update, delete)
    project_results = {}
    
    for operation in operations:
        print(f"\nRunning PROJECT {operation.upper()} performance tests...")
        project_results[operation] = run_experiment("project", operation, object_counts)
    
    # Create and save separate figures
    create_separate_figures(todo_results, project_results)