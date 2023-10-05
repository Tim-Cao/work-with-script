import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from liferay.jira.jira_connection import get_jira_connection
from liferay.jira.jira_constants import *
from liferay.jira.jira_util import *


def add_test_automation_ticket(
    story_ticket, test_description, field_and_name, priority, test_scenario, component, jira_connection, project_key
):
    print("Creating the Jira ticket...")

    if (project_key == "LPS"):
            issue_dict = {
                "project": {"key": "LPS"},
                "summary": "Automate " + field_and_name,
                "description": "+*Test Description:*+\n"
                + story_ticket 
                + ": " 
                + test_description 
                + "\n \n"
                + "+*Test Priority:*+\n"
                + "This is a priority "
                + priority 
                + " test. \n \n"
                + "+*Test Scenario (BDD):*+\n"
                + test_scenario 
                + "\n \n"
                + "+*Test Steps:*+\n \n"
                + "(i)	Once you complete your test, please do the following: \n"
                + "* Run SF locally and fix any SF related errors. Fix them in the commit that caused it, do not make a separate SF commit! \n"
                + "* Attach the index.html of your passing test to the ticket \n"
                + "* Send your PR to [liferay-bpm-qa|https://github.com/liferay-bpm-qa] for review. Please use the following format: \n"
                + "** Title: LPS-${ticketNumber} | master \n"
                + "** Body: https://issues.liferay.com/browse/${ticketNumber} \n"
                + "** Example: https://github.com/timpak/liferay-portal/pull/264 \n\n"
                + "(?) For object related questions, please ask in #t-dxp-bpm-qa\n\n"
                ,
                "components": [{"name": component}],
                "issuetype": {"name": "Testing"},
            }
    else:
        raise Exception("Sorry, projects other than LPS were not implemented yet.")

    return jira_connection.create_issue(fields=issue_dict)


def main(assigned, label, story_ticket, test_description, field_and_name, priority, test_scenario, component, project_key):
    jira_connection = get_jira_connection()

    issue = add_test_automation_ticket(
        story_ticket, test_description, field_and_name, priority, test_scenario, component, jira_connection, project_key
    )

    assign_to_me(assigned, jira_connection, issue)

    add_label(issue, label)

    print("Successful")

    print(f"{JIRA_INSTANCE}/browse/{issue.key}")
