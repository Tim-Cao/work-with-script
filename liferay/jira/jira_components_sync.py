import os
import sys

from jproperties import Properties

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from liferay.jira.jira_connection import get_jira_connection
from liferay.jira.jira_constants import *
from liferay.jira.jira_util import *


def sync_project_components(jira_connection, project_key):
    print(f"Getting the project {project_key} components...")

    components = get_project_components(jira_connection, project_key)

    component_names = []

    for component in components:
        if "Archive" in component.name:
            pass

        else:
            component_names.append(component.name)

    components = ""

    for component_name in component_names:
        components += f"('{component_name}', '{component_name}'),"

    print(f"Updating the project {project_key} components...")

    jira_components = Properties()

    jira_components[f"{project_key}_COMPONENTS"] = str(components)

    with open(
        os.path.join(
            os.path.dirname(__file__), "dependencies/jira_components.properties"
        ),
        "ab",
    ) as project_components:
        jira_components.store(project_components, encoding="utf-8")


def main():
    jira_connection = get_jira_connection()

    if not os.path.exists(os.path.join(os.path.dirname(__file__), "dependencies/")):
        os.mkdir(os.path.join(os.path.dirname(__file__), "dependencies/"))

    open(
        os.path.join(
            os.path.dirname(__file__), "dependencies/jira_components.properties"
        ),
        "w",
    )

    sync_project_components(jira_connection, "COMMERCE")

    sync_project_components(jira_connection, "LPS")

    sync_project_components(jira_connection, "LRQA")

    sync_project_components(jira_connection, "LRAC")

    print("Successfully...")
