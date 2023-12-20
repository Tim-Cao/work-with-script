import os
import sys

from jira import JIRA

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from liferay.jira.jira_constants import *
from liferay.util.credentials import get_credentials


def get_jira_connection():
    print("Jira authorizing...")

    return JIRA(
        JIRA_INSTANCE,
        options={"headers": {"Accept": "*/*"}},
        basic_auth=(get_credentials("JIRA_USER_NAME"), get_credentials("JIRA_TOKEN")),
    )
