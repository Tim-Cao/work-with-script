import os
import sys

from github import Github

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from liferay.util.credentials import get_credentials


def get_github_connection():
    return Github(get_credentials("GITHUB_TOKEN"))