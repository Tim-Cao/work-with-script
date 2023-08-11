# Script to write comments in ticket

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from liferay.jira.jira_connection import get_jira_connection
from liferay.jira.jira_constants import *
from liferay.jira.jira_util import *


def type_comments_type():
    retry = 0
    while True:
        retry += 1

        type = input("Enter the comments type: ")

        if type in ["PID", "FID", "NID", "PF", "FF", "NF", "R", "RU", "TV"]:
            return type
        elif retry == 3:
            exit("Retry exceeded 3 times")
        else:
            print("The comments types should be PID, FID, NID, PF, FF, NF, R, RU or TV.")

            continue

if __name__ == "__main__":
    ticket_number = input("Enter the jira ticket number: ")

    comments_type = type_comments_type()

    jira_connection = get_jira_connection()

    comment_template = generate_comment(comments_type)

    comment_id = jira_connection.add_comment(ticket_number, comment_template)

    print(JIRA_INSTANCE + "/browse/" + ticket_number + "?focusedCommentId=" + str(comment_id))