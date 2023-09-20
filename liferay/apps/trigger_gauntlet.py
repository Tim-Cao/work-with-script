import os
import pathlib
import git

from datetime import date
from github import Github
from jira import JIRA


# Create issue for gauntlet testing
user = 'email'
apikey = 'API Token'
server = 'https://liferay.atlassian.net/'

options = {
 'server': server
}
jira_connection = JIRA(options, basic_auth=(user,apikey))

today = date.today()
issue_dict = {
    'project': {'key': 'LRQA'},
    'summary': '7.3.x Gauntlet ' + str(today) + ' Daily',
    'description': 'Detailed ticket description.',
    'components': [{'name': 'Gauntlet Testing'}],
    'issuetype': {'name': 'Gauntlet Testing'},
}

new_issue = jira_connection.create_issue(fields=issue_dict)

print("Create issue successfully ")

# Update local branch
local_dir = '/home/liferay/project/liferay-portal-ee-7.3.x/'
repo = git.Repo(local_dir)
origin = repo.remote(name='origin')
origin.pull('7.3.x')

# Create a new branch for testing
#existing_branch = repo.heads['7.3.x']
#existing_branch.checkout(b='7.3.x-qa-test')
new_branch = repo.create_head('7.3.x-qa-' + new_issue.key[-5:])
new_branch.checkout()

print("Update local branch successfully")

# Add and Commit a empty file
repo_dir = os.path.join(local_dir)
file_name = os.path.join(repo_dir, "temp.temp")
open(file_name, "wb").close()
repo.index.add([file_name])
repo.index.commit(f'{new_issue.key} TEMP for gauntlet testing')
origin.push(new_branch)

print("Add and Commit a empty file successfully")

# Create a pull request for gauntlet testing
#access_token = (pathlib.Path().home() / ".github_access_token").read_text()
access_token = 'github-personal-access-token'
repo_name = 'liferay-portal-ee'
user_name = 'username'

g = Github(access_token)

repo = g.get_user(user_name).get_repo(repo_name)

base_branch = '7.3.x'
body= server + "/browse/" + new_issue.key
branch_name = new_branch
head = user_name + ":" + '7.3.x-qa-' + new_issue.key[-5:]
title = new_issue.key + ' | ' + '7.3.x'

pull_request = repo.create_pull(title=title,body=body,head=head,base=base_branch)

pull_request.create_issue_comment("ci:test:gauntlet-bucket")

print("Create a pull request for gauntlet testing successfully")

# Update the description of Gauntlet ticket
new_issue.update(description = pull_request.html_url)

print("Update ticket successfully")