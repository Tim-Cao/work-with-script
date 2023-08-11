import sys
import os

from git import Repo

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from liferay.util.credentials import get_credentials

def delete_temp_branch(local_repo):
    try:
        local_repo.delete_head("temp_branch", force=True)
    except Exception:
        pass

def fetch_remote_branch_as_temp_branch(local_repo,pull_request):
    try:
        local_repo.create_remote(pull_request.head.user.login, url=pull_request.head.repo.ssh_url)
    except Exception:
        pass

    local_repo.remote(name=str(pull_request.head.user.login)).fetch("refs/heads/" + str(pull_request.head.ref) + ":refs/heads/" + "temp_branch")

def get_local_repo():
    return Repo(get_credentials("LOCAL_REPO_PATH"))

def get_pull_request(remote_repo, pr_number):
    return remote_repo.get_pull(int(pr_number))

def get_remote_repo(github_connection, repo_name):
    return github_connection.get_repo(repo_name)

def push_branch_to_origin(local_repo, local_branch, remote_branch):
    local_repo.remote(name="origin").push("refs/heads/" + local_branch + ":refs/heads/" + remote_branch, force=True)
