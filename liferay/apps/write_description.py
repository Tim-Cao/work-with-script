import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from liferay.jira.jira_connection import get_jira_connection
from liferay.jira.jira_constants import *
from liferay.jira.jira_util import *


def main(description, ticket_number):
    jira_connection = get_jira_connection()

    issue = jira_connection.issue(ticket_number)

    print("Writing description...")

    issue.update(description=description)

    print("Successful")

    print(f"{JIRA_INSTANCE}/browse/{ticket_number}")
