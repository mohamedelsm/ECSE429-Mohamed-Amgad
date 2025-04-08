Feature: Manage Projects in the Todo List Manager

    As a user, I want to create and manage projects so that I can organize my tasks better.
            
    Scenario Outline: Create a new project (Normal Flow)
        When a user creates a project with title <title>, description <description>, and active status <active>
        Then the project with title <title> is created with the correct details
        And the user is notified of the success

        Examples:
            | title              | description            | active |
            | "API Development"  | "Develop API features" | true   |

    Scenario Outline: Create a project with only a title (Alternative Flow)
        When the user creates a project with the title <new_title>
        Then the project is created with the title <new_title> and default values for description and active status
        And the user is notified of the success
        
        Examples:
            | new_title         |
            | "API V2"          |

    Scenario Outline: Create a project while manually assigning an ID (Error Flow)
        Given a project with id <existing_id> already exists
        When the user tries to create a new project with id <existing_id>, title <title>, description <description>, and active status <active>
        Then the user is notified of the error

        Examples:
            | existing_id | title              | description                 | active |
            | 1           | "UI Redesign"      | "Create new user interface" | true   |
