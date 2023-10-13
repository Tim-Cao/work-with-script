import json
import os
import sys

import requests
from jsonpath_ng.ext import parse

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from liferay.jira.jira_connection import get_jira_connection
from liferay.jira.jira_constants import *
from liferay.jira.jira_util import *
from liferay.testray.testray_connection import get_testray_connection
from liferay.testray.testray_constants import *


def create_bug_ticket(
     bug_type,component,description,jira_connection,project_key,summary
):
    print("Creating the Jira ticket...")

    if (project_key == "LPS"):
            issue_dict = {
                "project": {"key": "LPS"},
                "summary": summary,
                "description": description,
                "components": [{"name": component}],
                "issuetype": {"name": "Bug"},
                "customfield_10240": {"value": bug_type},
                "versions": [{"name": "Master"}],
            }
    else:
        raise Exception("Sorry, projects other than LPS were not implemented yet.")

    return jira_connection.create_issue(fields=issue_dict)

def main(bug_type,component,description,label,project_key,summary):
    jira_connection = get_jira_connection()

    issue = create_bug_ticket(
        bug_type,component,description,jira_connection,project_key,summary
    )

    add_label(issue, label)

    print("Successful")

    print(f"{JIRA_INSTANCE}/browse/{issue.key}")
