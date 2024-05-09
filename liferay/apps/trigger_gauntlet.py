import os
import sys
from datetime import date

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from liferay.git.git_util import *
from liferay.git.github_connection import *
from liferay.jira.jira_connection import get_jira_connection
from liferay.jira.jira_constants import *
from liferay.jira.jira_util import *
from liferay.util.credentials import get_credentials


def create_gaunlet_pr(local_repo, remote_branch, target_branch, ticket_number):
    g = get_github_connection()

    remote_repo = get_remote_repo(
        g, f'{get_credentials("GITHUB_USER_NAME")}/liferay-portal-ee'
    )

    push_branch_to_origin(local_repo, "temp_branch", remote_branch)

    body = f"{JIRA_INSTANCE}/browse/{ticket_number}"
    head = f'{get_credentials("GITHUB_USER_NAME")}:{remote_branch}'
    title = f"{ticket_number} | {target_branch}"

    return remote_repo.create_pull(
        title=title, body=body, head=head, base=target_branch
    )


def create_gauntlet_ticket(target_branch):
    jira_connection = get_jira_connection()

    today = date.today()

    issue_dict = {
        "project": {"key": "LRQA"},
        "summary": f"{target_branch} Gauntlet {today} Daily",
        "components": [{"name": "Gauntlet Testing"}],
        "issuetype": {"name": "Gauntlet Testing"},
    }

    print("Creating the Jira ticket...")

    return jira_connection.create_issue(fields=issue_dict)


def create_testing_branch(local_repo, target_branch):
    clean_working_tree(local_repo)

    checkout(target_branch, local_repo)

    clean_working_tree(local_repo)

    delete_temp_branch(local_repo)

    update_local_branch(local_repo, target_branch)

    create_branch("temp_branch", local_repo)

    checkout("temp_branch", local_repo)


def make_changes_for_gauntlet_test(commit_message, file_name, repo):
    print("Making changes for gauntlet test...")

    with open(file_name, "w"):
        pass

    repo.index.add([file_name])
    repo.index.commit(commit_message)


def paste_pr_to_ticket(gauntlet_ticket, pr):
    gauntlet_ticket.update(description=pr.html_url)


def run_gauntlet(pr):
    print("Run ci:test:gauntlet-bucket")

    pr.create_issue_comment("ci:test:gauntlet-bucket")


def main(legacy_repo_path, target_branch):
    gauntlet_ticket = create_gauntlet_ticket(target_branch)

    remote_branch = f"{target_branch}-qa-{gauntlet_ticket.key[-5:]}"

    local_repo = Repo(legacy_repo_path)

    create_testing_branch(local_repo, target_branch)

    make_changes_for_gauntlet_test(
        f"{gauntlet_ticket.key} TEMP for gauntlet testing",
        os.path.join(legacy_repo_path, "temp.text"),
        local_repo,
    )

    pr = create_gaunlet_pr(
        local_repo, remote_branch, target_branch, gauntlet_ticket.key
    )

    run_gauntlet(pr)

    paste_pr_to_ticket(gauntlet_ticket, pr)

    print(f"\033[1;32mSuccessful\033[0m")

    print(f"{JIRA_INSTANCE}/browse/{gauntlet_ticket.key}")

    print(pr.html_url)
