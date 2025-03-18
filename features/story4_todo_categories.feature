Feature: Manage Todo Categories in the Todo List Manager
    As a user, I want to manage categories for my todos so that I can organize them better.

    Background: Server is running, and initial data is loaded
        Given the server is running
        And a todo with title "Categorized Todo" exists
        And a category with title "Test Category" exists

    Scenario Outline: Add category to todo (Normal Flow)
        Given a todo with title <todo_title> exists
        And a category with title <category_title> exists
        When the user adds the category to the todo
        Then the category is successfully associated with the todo
        And the todo's categories include <category_title>
        And the user is notified of the successful association

        Examples:
            | todo_title             | category_title          |
            | "Work Report"          | "Office Tasks"          |
            | "Grocery Shopping"     | "Personal Errands"      |
            | "Fix Bug #123"         | "Development"           |
            | "Team Meeting Notes"   | "Meetings"              |

    Scenario Outline: Get categories of a todo (Alternative Flow)
        Given a todo with title <todo_title> exists
        And a category with title <category_title> exists
        When the user adds the category to the todo
        And the user requests the todo's categories
        Then the response includes the category <category_title>
        And the user is notified of the successful retrieval

        Examples:
            | todo_title             | category_title          |
            | "Daily Standup"        | "Team Activities"       |
            | "Code Review"          | "Development Tasks"     |
            | "Doctor Appointment"   | "Health"                |
            | "Birthday Party"       | "Social Events"         |

    Scenario Outline: Add non-existent category (Error Flow)
        Given a todo with title <todo_title> exists
        When the user tries to add a category with id <invalid_id> to the todo
        Then the user is notified of the error

        Examples:
            | todo_title             | invalid_id  |
            | "Important Task"       | "999999"    |
            | "Urgent Meeting"       | "888888"    |
            | "Project Deadline"     | "777777"    |