import os
import re
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from liferay.git.git_util import *
from liferay.git.github_connection import *
from liferay.jira.jira_constants import *
from liferay.util.credentials import get_credentials


def add_comments_in_failure_pr(new_pr_link, pull_request):
    pull_request.create_issue_comment("See " + new_pr_link)
    pull_request.create_issue_comment("ci:close")

def add_comments_in_new_pr(failure_pr_link, pull_request):
    time.sleep(3)

    comments = "In order to not clog up ci resources, I'm sending the PR directly. Failure cases are unrelated to changes in this PR.\n\nSee "  + failure_pr_link

    pull_request.create_issue_comment("ci:reopen")
    pull_request.create_issue_comment(comments)

def create_pr_to_brianchan(failure_pr, github_connection):
    print("Creating the pull request...")

    ticket_numbers = re.findall("[A-Z]+\-\d+", failure_pr.title)

    jira_links = ""

    for ticket_number in ticket_numbers:
        jira_links += JIRA_INSTANCE + "/browse/" + str(ticket_number) + "\n"

    head = get_credentials("GITHUB_USER_NAME") + ":" + str(failure_pr.head.ref)

    body = jira_links + "\n" + "@" + str(failure_pr.user.login)

    brianchan_repo = get_remote_repo(github_connection,"brianchandotcom/liferay-portal")

    return brianchan_repo.create_pull(title=failure_pr.title, head=head,  base="master", body=body, maintainer_can_modify=True)

def main(pull_request_number):
    local_repo = get_local_repo()

    delete_temp_branch(local_repo)

    g = get_github_connection()

    team_repo = get_remote_repo(g, get_credentials("TEAM_REPO_NAME"))

    failure_pr = get_pull_request(team_repo, pull_request_number)

    fetch_remote_branch_as_temp_branch(local_repo, failure_pr)

    push_branch_to_origin(local_repo, "temp_branch", failure_pr.head.ref)

    new_pr = create_pr_to_brianchan(failure_pr, g)

    delete_temp_branch(local_repo)

    print("Writing comments...")

    add_comments_in_new_pr(failure_pr.html_url, new_pr)

    add_comments_in_failure_pr(new_pr.html_url, failure_pr)

    print(new_pr.html_url)
