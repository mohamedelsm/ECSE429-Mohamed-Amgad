import threading
import time
import psutil
import statistics
import pandas as pd
import matplotlib.pyplot as plt
import requests
import random
import string

BASE_URL = "http://localhost:4567"

def random_string(length=10):
    """Generate a random string for test data"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

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


def run_experiment(operation, object_counts):
    """Run experiments with resource monitoring during execution"""
    results = []
    monitor = ResourceMonitor(sample_interval=0.1)  # Sample every 100ms
    
    for count in object_counts:
        # Create objects first if needed
        if operation != "create":
            todos = []
            for _ in range(count):
                todo = create_todo()
                if todo:
                    todos.append(todo["id"])
        
        # Start monitoring
        monitor.start_monitoring()
        
        # Time the operation
        start_time = time.time()
        
        if operation == "create":
            for _ in range(count):
                create_todo()
        elif operation == "delete":
            for todo_id in todos:
                delete_todo(todo_id)
        elif operation == "update":
            for todo_id in todos:
                update_todo(todo_id)
        
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
        
        print(f"Completed {operation} test with {count} objects in {duration:.2f} seconds")
        print(f"  CPU: avg={stats['cpu_avg']:.1f}%, max={stats['cpu_max']:.1f}%")
        print(f"  Memory: avg={stats['memory_avg']:.1f}MB, max={stats['memory_max']:.1f}MB")
        
        # Small delay to let system stabilize
        time.sleep(2)
    
    return results

def visualize_results(results_dict):
    """Create visualizations of the results"""
    df = pd.DataFrame()
    for operation, results in results_dict.items():
        op_df = pd.DataFrame(results)
        op_df['operation'] = operation
        df = pd.concat([df, op_df], ignore_index=True)
    
    # Create plots
    plt.figure(figsize=(15, 12))
    
    # Plot 1: Total time by operation and count
    plt.subplot(2, 2, 1)
    for operation in df['operation'].unique():
        op_df = df[df['operation'] == operation]
        plt.plot(op_df['count'], op_df['time_seconds'], marker='o', label=operation)
    plt.title('Total Time vs Object Count')
    plt.xlabel('Number of Objects')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(True)
    
    # Plot 2: Average time per operation
    plt.subplot(2, 2, 2)
    for operation in df['operation'].unique():
        op_df = df[df['operation'] == operation]
        plt.plot(op_df['count'], op_df['avg_time_per_op'], marker='o', label=operation)
    plt.title('Average Time per Operation vs Object Count')
    plt.xlabel('Number of Objects')
    plt.ylabel('Time per Operation (seconds)')
    plt.legend()
    plt.grid(True)
    
    # Plot 3: CPU Usage (avg)
    plt.subplot(2, 2, 3)
    for operation in df['operation'].unique():
        op_df = df[df['operation'] == operation]
        plt.plot(op_df['count'], op_df['cpu_avg_percent'], marker='o', label=operation)
    plt.title('Average CPU Usage vs Object Count')
    plt.xlabel('Number of Objects')
    plt.ylabel('CPU Usage (%)')
    plt.legend()
    plt.grid(True)
    
    # Plot 4: Memory Usage (avg)
    plt.subplot(2, 2, 4)
    for operation in df['operation'].unique():
        op_df = df[df['operation'] == operation]
        plt.plot(op_df['count'], op_df['memory_avg_mb'], marker='o', label=operation)
    plt.title('Average Memory Usage vs Object Count')
    plt.xlabel('Number of Objects')
    plt.ylabel('Memory Used (MB)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('tests/performance_results.png')
    plt.show()
    
    # Save detailed results to CSV
    df.to_csv('tests/performance_results.csv', index=False)
    print("Results saved to performance_results.csv and performance_results.png")

if __name__ == "__main__":
    # Define the object counts to test with
    object_counts = [10, 50, 100, 200, 500, 1000]
    
    # Run experiments for create, update, and delete operations
    results = {}
    operations = ["create", "update", "delete"]
    
    for operation in operations:
        print(f"\nRunning {operation.upper()} performance tests...")
        results[operation] = run_experiment(operation, object_counts)
    
    # Visualize and save results
    visualize_results(results)