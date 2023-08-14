# Script to create PR and forward

import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from liferay.git.git_util import *
from liferay.git.github_connection import *
from liferay.jira.jira_constants import *
from liferay.util.credentials import get_credentials


def create_pr_to_team(jira_ticket_number, local_branch):
    base = "master"

    title = jira_ticket_number + " | " + base

    head = get_credentials("GITHUB_USER_NAME") + ":" + local_branch

    body = JIRA_INSTANCE + "/browse/" + jira_ticket_number + "\n" + "\n" + "@" + get_credentials("GITHUB_REVIEWER_NAME")

    g = get_github_connection()

    team_repo = get_remote_repo(g, get_credentials("TEAM_REPO_NAME"))

    return team_repo.create_pull(title=title, head=head,  base=base, body=body, maintainer_can_modify=True)

def forward_pull_request(pull_request):
    time.sleep(3)

    pull_request.create_issue_comment("ci:forward")

if __name__ == "__main__":
    local_branch = input("Enter the local branch name: ")

    local_repo = get_local_repo()

    push_branch_to_origin(local_repo, local_branch, local_branch)

    pr = create_pr_to_team(input("Enter the jira ticket number: "), local_branch)

    forward_pull_request(pr)

    print(pr.html_url)