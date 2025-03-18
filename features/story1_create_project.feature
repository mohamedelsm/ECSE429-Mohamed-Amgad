Feature: Manage Projects in the Todo List Manager

    As a user, I want to create and manage projects so that I can organize my tasks better.

    Background: Server is running, and initial data is loaded
        Given the server is running
            
    Scenario Outline: Create a new project (Normal Flow)
        When a user creates a project with title <title>, description <description>, and active status <active>
        Then the project with title <title> is created with the correct details
        And the user is notified of the successful creation

        Examples:
            | title              | description            | active |
            | "API Development"  | "Develop API features" | true   |

    Scenario Outline: Update an existing project (Alternative Flow)
        Given a project with id <existing_id> already exists
        When the user updates the project with new title <new_title>, description <new_description>, and active status <new_active>
        Then the project with new title <new_title> is updated with the correct details
        And the user is notified of the successful update

        Examples:
            | existing_id    | new_title         | new_description          | new_active |
            | 1              | "API V2"          | "Implement version 2"    | true       |

    Scenario Outline: Create a project while manually assigning an ID (Error Flow)
        Given a project with id <existing_id> already exists
        When the user tries to create a new project with id <existing_id>, title <title>, description <description>, and active status <active>
        Then the user is notified of the error

        Examples:
            | existing_id | title              | description                 | active |
            | 1           | "UI Redesign"      | "Create new user interface" | true   |