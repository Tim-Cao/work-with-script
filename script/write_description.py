# Script to write comments in ticket

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from liferay.jira.jira_connection import get_jira_connection
from liferay.jira.jira_constants import *
from liferay.jira.jira_util import *


def type_description_type():
    retry = 0
    while True:
        retry += 1

        type = input("Enter the description type: ")

        if type in ["STR", "TC"]:
            return type
        elif retry == 3:
            exit("Retry exceeded 3 times")
        else:
            print("The description types should be STR or TC.")

            continue

if __name__ == "__main__":
    ticket_number = input("Enter the jira ticket number: ")

    description_type = type_description_type()

    jira_connection = get_jira_connection()

    issue = jira_connection.issue(ticket_number)

    description_template = generate_description(description_type)

    issue.update(description = description_template)

    print(JIRA_INSTANCE + "/browse/" + ticket_number)