Feature: Delete Todos in the Todo List Manager

    As a user, I want to delete todos so that I can remove completed or unnecessary tasks.

    Background: Server is running, and initial data is loaded
        Given the server is running
        And a todo with title "Todo to Delete" and description "Will be deleted" exists

    Scenario Outline: Delete an existing todo (Normal Flow)
        Given a todo with title <title> and description <description> exists
        When the user deletes the todo
        Then the todo is successfully deleted
        And subsequent retrieval of the todo returns not found
        And the user is notified of the successful deletion

        Examples:
            | title                  | description                    |
            | "Completed Task"       | "This task is done"           |
            | "Cancelled Meeting"    | "Meeting was cancelled"       |

    Scenario Outline: Verify todo removal from lists (Alternative Flow)
        Given a todo with title <title> and description <description> exists
        When the user deletes the todo
        Then the todo is successfully deleted
        And the todo no longer appears in the list of all todos
        And the user is notified of the successful deletion

        Examples:
            | title                  | description                    |
            | "Old Task"            | "Task to be removed"           |
            | "Obsolete Todo"       | "No longer needed"            |

    Scenario Outline: Delete already deleted todo (Error Flow)
        Given a todo with title <title> and description <description> exists
        When the user deletes the todo
        And the user attempts to delete the same todo again
        Then the user is notified of the error

        Examples:
            | title                  | description                    |
            | "Double Delete"        | "Try to delete twice"         |
            | "Already Gone"         | "Already deleted todo"        |