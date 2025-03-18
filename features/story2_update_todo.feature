Feature: Update Todos in the Todo List Manager
    As a user, I want to update my existing todos so that I can modify task details when needed.

  Background: Server is running, and initial data is loaded
    Given the server is running
    And a todo with title "Initial Todo" and description "Initial Description" exists

  Scenario Outline: Update todo title and description (Normal Flow)
    When the user updates the todo with new title "<new_title>" and new description "<new_description>"
    Then the todo with new title "<new_title>" is updated with the correct details
    And the user is notified of the successful update

    Examples:
      | new_title                | new_description                        |
      | "Updated Work Task"      | "Revised project documentation needed" |
      | "Modified Shopping List" | "Updated grocery list for party"       |

  Scenario Outline: Update todo using XML format (Alternative Flow)
    When the user updates the todo using XML format with title "<title>" and description "<description>"
    Then the todo with title "<title>" is updated with the correct details
    And the response is in XML format
    And the user is notified of the successful update

    Examples:
      | title              | description                     |
      | "XML Updated Task" | "Task updated using XML format" |

  Scenario Outline: Update non-existent todo (Error Flow)
    When the user tries to update a non-existent todo with id "<invalid_id>"
    Then the user is notified of the error

    Examples:
      | invalid_id |
      | "999999"   |
      | "888888"   |
