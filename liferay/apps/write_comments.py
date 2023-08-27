import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from liferay.jira.jira_connection import get_jira_connection
from liferay.jira.jira_constants import *
from liferay.jira.jira_util import *


def main(commit_id, description, env, ticket_number, type):
    jira_connection = get_jira_connection()

    comment_template = generate_comment(commit_id, description, env, type)

    print("Writing comments...")

    comment_id = jira_connection.add_comment(ticket_number, comment_template)

    print(JIRA_INSTANCE + "/browse/" + ticket_number + "?focusedCommentId=" + str(comment_id))