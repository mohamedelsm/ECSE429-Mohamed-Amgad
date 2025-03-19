from setup import start_api, is_api_running, stop_api

def before_scenario(context, scenario):
    print(f"\nStarting scenario: {scenario.name}")

def after_scenario(context, scenario):
    print(f"\nFinished scenario: {scenario.name}")

def before_feature(context, feature):
    print(f"Starting feature: {feature.name}")
    # Start the API server before each feature
    if not is_api_running():
        context.api_process = start_api()
    assert is_api_running(), "API did not start successfully."

def after_feature(context, feature):
    print(f"Finishing feature: {feature.name}")
    # Stop the API server after each feature
    if hasattr(context, 'api_process') and context.api_process:
        stop_api(context.api_process)
    else:
        print("No API process found to stop.")
    assert not is_api_running(), "API did not stop successfully."