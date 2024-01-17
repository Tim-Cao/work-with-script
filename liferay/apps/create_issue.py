import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from liferay.jira.jira_connection import get_jira_connection
from liferay.jira.jira_constants import *
from liferay.jira.jira_util import *


def create_issue(
    affects_versions,
    bug_type,
    component,
    description,
    issue_type,
    jira_connection,
    project_key,
    summary,
):
    print("Creating the Jira ticket...")

    if issue_type == "Bug":
        issue_dict = {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "components": [{"name": component}],
            "customfield_10240": {"value": bug_type},
            "issuetype": {"name": issue_type},
            "versions": [{"name": affects_versions}],
        }
    else:
        issue_dict = {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "components": [{"name": component}],
            "issuetype": {"name": issue_type},
        }

    return jira_connection.create_issue(fields=issue_dict)


def main(
    affects_versions,
    assigned,
    bug_type,
    component,
    description,
    issue_type,
    label,
    project_key,
    summary,
):
    jira_connection = get_jira_connection()

    issue = create_issue(
        affects_versions,
        bug_type,
        component,
        description,
        issue_type,
        jira_connection,
        project_key,
        summary,
    )

    assign_to_me(assigned, jira_connection, issue)

    add_label(issue, label)

    print(f"\033[1;32mSuccessful\033[0m")

    print(f"{JIRA_INSTANCE}/browse/{issue.key}")
