import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from liferay.git.git_util import *
from liferay.git.github_connection import *
from liferay.jira.jira_constants import *
from liferay.util.credentials import get_credentials


def create_pr_to_team(github_connection, jira_ticket_number, local_branch):
    print("Creating the pull request...")

    base = "master"

    title = jira_ticket_number + " | " + base

    head = get_credentials("GITHUB_USER_NAME") + ":" + local_branch

    body = (
        JIRA_INSTANCE
        + "/browse/"
        + jira_ticket_number
        + "\n"
        + "\n"
        + "@"
        + get_credentials("GITHUB_REVIEWER_NAME")
    )

    team_repo = get_remote_repo(github_connection, get_credentials("TEAM_REPO_NAME"))

    return team_repo.create_pull(
        title=title, head=head, base=base, body=body, maintainer_can_modify=True
    )


def forward_pull_request(pull_request):
    print("Run ci:forward...")

    time.sleep(3)

    pull_request.create_issue_comment("ci:forward")


def main(local_branch, jira_ticket_number):
    local_repo = get_local_repo()

    push_branch_to_origin(local_repo, local_branch, local_branch)

    g = get_github_connection()

    pr = create_pr_to_team(g, jira_ticket_number, local_branch)

    forward_pull_request(pr)

    print("Successful")

    print(pr.html_url)
