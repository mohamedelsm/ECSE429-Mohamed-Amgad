Feature: List projects
    As a user, I want to view a list of projects and filter them by their various fields.

    # Normal Flow: Successfully list all projects
    Scenario: List all projects
        When the user requests the list of projects
        Then all projects are displayed

    # Alternate Flow: Filter projects by active status
    Scenario Outline: List projects filtered by active status
        When the user filters the projects by active status <active_status>
        Then only projects with the active status <active_status> are displayed

        Examples:
            | active_status |
            | false         |

    # Error Flow: Attempt to filter projects by an invalid value for active status
    Scenario Outline: Filter projects by an invalid value for active status
        When the user filters the projects by active status <invalid_active_status>
        Then the user receives an empty list

        Examples:
            | invalid_active_status |
            | "cheese"              |
