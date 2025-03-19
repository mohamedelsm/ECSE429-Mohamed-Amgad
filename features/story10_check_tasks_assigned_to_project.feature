Feature: Check tasks assigned to a project
    As a user
    I want to view tasks assigned to a specific project
    So that I can track the work items associated with that project

    # Normal Flow: Successfully check tasks assigned to a project
    Scenario Outline: View all tasks assigned to a project
        Given a project with id <existing_id> already exists
        When the user checks the tasks assigned to the project with id <existing_id>
        Then the user is notified of the success

        Examples:
            | existing_id |
            | 1           |

    # Alternate Flow: Get a task with a particular id associated with a specific project
    Scenario Outline: Get a task associated with a project by ID
        Given a project with id <existing_project_id> already exists
        And a task with id <existing_task_id> is assigned to the project with id <existing_project_id>
        When the user retrieves the task with id <existing_task_id> from the project with id <existing_project_id>
        Then the user is notified of the success

        Examples:
            | existing_project_id | existing_task_id |
            | 1                   | 1                |

    # Error Flow: Attempt to check tasks for a non-existent project
    Scenario Outline: Attempt to check tasks with a non-existent id
        Given no project with id <nonexistent_id> exists
        When the user tries to check the task with <nonexistent_id> assigned to the project with id <existing_id>
        Then the user is notified of the error

        Examples:
            | nonexistent_id | existing_id |
            | 999            | 1          |
