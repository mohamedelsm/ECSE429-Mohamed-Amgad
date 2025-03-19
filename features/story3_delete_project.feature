Feature: Delete a project
    As a user, I want to delete an existing project, so that I can remove unnecessary or outdated projects

    Scenario Outline: Delete a project (Normal Flow)
        Given a project with id <existing_id> already exists
        When the user deletes the project with id <existing_id>
        Then the project with id <existing_id> is deleted successfully
        And the user is notified of the success

        Examples:
            | existing_id |
            | 1           |

    Scenario Outline: Verify removed project does not appear in project list
        Given that project with id <existing_id> has been deleted
        Then the project with id <existing_id> does not appear in the project list

        Examples:
            | existing_id |
            | 1           |

    # Error Flow: Attempt to delete a non-existing project
    Scenario Outline: Attempt to delete a non-existing project
        When the user tries to delete the project with id <non_existing_id>
        Then the user is notified of the error

        Examples:
            | non_existing_id |
            | 999             |