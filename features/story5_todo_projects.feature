Feature: Manage Todo Project Associations in the Todo List Manager
    As a user, I want to associate todos with projects so that I can organize related tasks together.

    Background: Server is running, and initial data is loaded
        Given the server is running
        And a todo with title "Project Task" exists
        And a project with title "Test Project" exists

    Scenario Outline: Associate todo with project (Normal Flow)
        Given a todo with title <todo_title> exists
        And a project with title <project_title> exists
        When the user adds the todo to the project
        Then the todo is successfully associated with the project
        And the project's tasks include the todo
        And the user is notified of the successful association

        Examples:
            | todo_title                     | project_title               |
            | "Implement Login Feature"      | "User Authentication"       |
            | "Design Database Schema"       | "Database Migration"        |
            | "Write Unit Tests"            | "Quality Assurance"         |
            | "Create API Documentation"     | "Documentation"             |

    Scenario Outline: Get project tasks (Alternative Flow)
        Given a todo with title <todo_title> exists
        And a project with title <project_title> exists
        When the user adds the todo to the project
        And the user requests the project's tasks
        Then the response includes the todo
        And the user is notified of the successful retrieval

        Examples:
            | todo_title                     | project_title               |
            | "Frontend Bug Fix"             | "Website Redesign"          |
            | "Update Dependencies"          | "System Maintenance"        |
            | "Review Pull Request"          | "Code Review Process"       |
            | "Deploy to Production"         | "Release Management"        |

    Scenario Outline: Associate with non-existent project (Error Flow)
        Given a todo with title <todo_title> exists
        When the user tries to add the todo to a project with id <invalid_id>
        Then the user is notified of the error

        Examples:
            | todo_title                     | invalid_id  |
            | "Critical Bug Fix"             | "999999"    |
            | "Security Patch"               | "888888"    |
            | "Performance Optimization"     | "777777"    |