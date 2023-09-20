import os
import sys

from git import Repo

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from liferay.util.credentials import get_credentials


def checkout(local_branch, local_repo):
    local_repo.heads[local_branch].checkout()


def clean_working_tree(local_repo):
    local_repo.head.reset(working_tree=True)


def create_branch(local_branch, local_repo):
    print(f"Creating branch {local_branch}...")

    return local_repo.create_head(local_branch)


def delete_temp_branch(local_repo):
    try:
        local_repo.delete_head("temp_branch", force=True)
    except Exception:
        pass


def fetch_remote_branch_as_temp_branch(local_repo, pull_request):
    try:
        local_repo.create_remote(
            pull_request.head.user.login, url=pull_request.head.repo.ssh_url
        )
    except Exception:
        pass

    print("Fetching the branch...")

    local_repo.remote(name=str(pull_request.head.user.login)).fetch(
        "refs/heads/" + str(pull_request.head.ref) + ":refs/heads/" + "temp_branch"
    )


def get_local_repo():
    return Repo(get_credentials("LOCAL_REPO_PATH"))


def get_pull_request(remote_repo, pr_number):
    return remote_repo.get_pull(int(pr_number))


def get_remote_repo(github_connection, repo_name):
    return github_connection.get_repo(repo_name)


def push_branch_to_origin(local_repo, local_branch, remote_branch):
    print("Pushing to origin...")

    local_repo.remote(name="origin").push(
        "refs/heads/" + local_branch + ":refs/heads/" + remote_branch, force=True
    )


def update_local_branch(local_repo, target_branch):
    print("Pulling from upstream...")

    local_repo.remotes["upstream"].pull(target_branch)
