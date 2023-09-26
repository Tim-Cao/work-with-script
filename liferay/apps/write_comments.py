import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from liferay.jira.jira_connection import get_jira_connection
from liferay.jira.jira_constants import *
from liferay.jira.jira_util import *


def main(comments, ticket_number):
    jira_connection = get_jira_connection()

    print("Writing comments...")

    comment_id = jira_connection.add_comment(ticket_number, comments)

    print("Successful")

    print(f"{JIRA_INSTANCE}/browse/{ticket_number}?focusedCommentId={comment_id}")
