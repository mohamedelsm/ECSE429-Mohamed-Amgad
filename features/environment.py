def before_scenario(context, scenario):
    print(f"\nStarting scenario: {scenario.name}")

def after_scenario(context, scenario):
    print(f"\nFinished scenario: {scenario.name}")