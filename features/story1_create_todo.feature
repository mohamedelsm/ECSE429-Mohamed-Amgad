Feature: Manage Todos in the Todo List Manager
    As a user, I want to create and manage todos so that I can track my tasks effectively.

  Background: Server is running, and initial data is loaded
    Given the server is running

  Scenario Outline: Create a new todo (Normal Flow)
    When a user creates a todo with title "<title>" and description "<description>"
    Then the todo with title "<title>" is created with the correct details
    And the user is notified of the successful creation

    Examples:
      | title              | description                      |
      | "Work Tasks"       | "Complete project documentation" |
      | "Shopping List"    | "Buy groceries for the week"     |
      | "Home Maintenance" | "Fix the leaking faucet"         |
      | "Study Plan"       | "Prepare for upcoming exams"     |

  Scenario Outline: Create a todo with only title (Alternative Flow)
    When a user creates a todo with only title "<title>"
    Then the todo with title "<title>" is created with the correct details
    And the todo has an empty description
    And the user is notified of the successful creation

    Examples:
      | title                |
      | "Team Meeting"       |
      | "Doctor Appointment" |
      | "Call Mom"           |

  Scenario Outline: Create a todo without title (Error Flow)
    When a user tries to create a todo with description "<description>" but no title
    Then the user is notified of the error
    And the error message indicates the title field is mandatory

    Examples:
      | description                             |
      | "This todo should fail without a title" |
      | "Another invalid todo attempt"          |
