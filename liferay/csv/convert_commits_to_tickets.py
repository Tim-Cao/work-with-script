import os
import subprocess
import sys

import pandas as pd

root = os.path.join(os.path.dirname(__file__), "../../")

sys.path.append(root)

from liferay.git.git_util import *
from liferay.git.github_connection import *
from liferay.jira.jira_connection import get_jira_connection
from liferay.jira.jira_constants import *


def main(base, head, repo_name):
    repo = get_remote_repo(get_github_connection(), repo_name)

    jira_connection = get_jira_connection()

    print("Converting...")

    df = pd.DataFrame(columns=["Ticket_Number", "Description"])

    df1 = pd.DataFrame(columns=["Ticket Number", "Summary", "Components", "Issue Type"])

    commits = repo.get_commits(head)

    for commit in commits:
        if commit.sha != base:
            if "LRQA" in commit.commit.message.strip().replace("\n", " "):
                continue
            elif "LRAC" in commit.commit.message.strip().replace("\n", " "):
                continue
            elif "LRP" in commit.commit.message.strip().replace("\n", " "):
                continue
            elif "LRCI" in commit.commit.message.strip().replace("\n", " "):
                continue
            elif "POSHI" in commit.commit.message.strip().replace("\n", " "):
                continue
            elif "artifact:ignore" in commit.commit.message.strip().replace("\n", " "):
                continue

            list = commit.commit.message.strip().replace("\n", " ").split(" ", 1)

            if len(list) == 1:
                list.append("NaN")

            df.loc[len(df)] = list
        else:
            break

    df2 = df.loc[
        ~(
            df.Ticket_Number.str.match("^[A-Z]+-[0-9]+.+")
            | df.Ticket_Number.str.contains("build.gradle")
            | df.Description.str.contains("Release Apps")
        )
    ]

    df2 = df2.rename(
        columns={"Ticket_Number": "Ticket Number", "Description": "Summary"}
    )

    df = df.loc[df.Ticket_Number.str.match("^[A-Z]+-[0-9]+.+")]

    df = df.drop_duplicates(subset="Ticket_Number", keep="first").reset_index(drop=True)

    for row in df.itertuples():
        try:
            issue = jira_connection.issue(row.Ticket_Number)
        except:
            df1.loc[len(df1)] = [row.Ticket_Number, row.Description, "", ""]

            continue

        issue_type = issue.fields.issuetype.name

        if issue_type == "Testing":
            continue
        elif issue_type == "Technical Testing":
            continue

        summary = issue.fields.summary

        component_name = []

        for component in issue.fields.components:
            component_name.append(component.name)

        link = f"{JIRA_INSTANCE}/browse/{row.Ticket_Number}"

        df1.loc[len(df1)] = [
            f'=HYPERLINK("{link}", "{row.Ticket_Number}")',
            summary,
            component_name,
            issue_type,
        ]

    df3 = pd.concat([df1, df2])

    df3.to_csv(os.path.join(root, "root_cause.csv"), index=False)

    print("Successful...")

    print(f"https://github.com/{repo_name}/compare/{base}...{head}")
