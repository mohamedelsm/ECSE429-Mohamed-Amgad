import os
import random
import subprocess

def get_feature_files(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.feature')]

def run_features_in_random_order(directory):
    feature_files = get_feature_files(directory)
    random.shuffle(feature_files)
    for feature in feature_files:
        result = subprocess.run(['behave', feature])
        if result.returncode != 0:
            print(f"Feature {feature} failed.")
            break

if __name__ == "__main__":
    features_dir = 'features'  # Adjust this path as needed
    run_features_in_random_order(features_dir)