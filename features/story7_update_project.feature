Feature: Update a project

    As a user, I want to update an existing project, so that I can modify its details

    Scenario Outline: Update a project with all details (Normal Flow)
        Given a project with id <existing_id> already exists
        When the user updates the project with id <existing_id> with new name <new_name>, content <new_content>, and status <new_status>
        Then the project is updated with the new details
        And the user is notified of the success

        Examples:
            | existing_id | new_name         | new_content        | new_status |
            | 1           | "project V2"     | "Updated content"  | false     |

    Scenario Outline: Update only the name of a project (Alternative Flow)
        Given a project with id <existing_id> already exists
        When the user updates the project with id <existing_id> with the name <new_name>
        Then the project is updated with the name <new_name> and the rest of the details remain the same
        And the user is notified of the success

        Examples:
            | existing_id | new_name           |
            | 1           | "Renamed project"  |

    Scenario Outline: Attempt to update a non-existent project (Error Flow)
        Given no project with id <nonexistent_id> exists
        When the user tries to update the project with id <nonexistent_id>, name <new_name>, content <new_content>, and status <new_status>
        Then the user is notified of the error

        Examples:
            | nonexistent_id | new_name         | new_content      | new_status |
            | 999            | "project V3"     | "New content"    | true   |
