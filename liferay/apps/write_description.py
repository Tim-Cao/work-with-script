import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from liferay.jira.jira_connection import get_jira_connection
from liferay.jira.jira_constants import *
from liferay.jira.jira_util import *


def main(ticket_number, type):
    jira_connection = get_jira_connection()

    issue = jira_connection.issue(ticket_number)

    description_template = generate_description(type)

    print("Writing description...")

    issue.update(description=description_template)

    print("Successful")

    print(JIRA_INSTANCE + "/browse/" + ticket_number)
