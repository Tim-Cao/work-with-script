import json
import os
import sys

import requests
from jsonpath_ng.ext import parse

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from liferay.jira.jira_connection import get_jira_connection
from liferay.jira.jira_constants import *
from liferay.jira.jira_util import *
from liferay.testray.testray_connection import get_testray_connection
from liferay.testray.testray_constants import *


def add_test_fix_ticket(
    case_error, case_name, case_result_id, component, jira_connection, project_key
):
    print("Creating the Jira ticket...")

    if project_key == "LPS":
        issue_dict = {
            "project": {"key": "LPS"},
            "summary": "Investigate failure in " + case_name,
            "description": "*Error Message*\n\n{code:java}"
            + case_error
            + "{code}\n\n*Affect Tests*\n["
            + case_name
            + "|"
            + TESTRAY_INSTANCE
            + "/home/-/testray/case_results/"
            + case_result_id
            + "]",
            "components": [{"name": component}],
            "issuetype": {"name": "Task"},
        }
    elif project_key == "LRAC":
        issue_dict = {
            "project": {"key": "LRAC"},
            "summary": "Investigate failure in " + case_name,
            "description": "*Error Message*\n\n{code:java}"
            + case_error
            + "{code}\n\n*Affect Tests*\n["
            + case_name
            + "|"
            + TESTRAY_INSTANCE
            + "/home/-/testray/case_results/"
            + case_result_id
            + "]",
            "components": [{"name": component}],
            "issuetype": {"name": "Task"},
        }
    elif project_key == "COMMERCE":
        issue_dict = {
            "project": {"key": "COMMERCE"},
            "summary": "Investigate failure in " + case_name,
            "description": "*Error Message*\n\n{code:java}"
            + case_error
            + "{code}\n\n*Affect Tests*\n["
            + case_name
            + "|"
            + TESTRAY_INSTANCE
            + "/home/-/testray/case_results/"
            + case_result_id
            + "]",
            "issuetype": {"name": "Task"},
        }

    return jira_connection.create_issue(fields=issue_dict)


def get_case_component(case_result):
    jsonpath_expression = parse("$..testrayComponentName")

    return jsonpath_expression.find(case_result)[0].value


def get_case_error(case_result):
    jsonpath_expression = parse("$..errors")

    return jsonpath_expression.find(case_result)[0].value


def get_case_name(case_result):
    jsonpath_expression = parse("$..testrayCaseName")

    return jsonpath_expression.find(case_result)[0].value


def get_case_result(auth, case_result_id):
    print("Getting the case result...")

    testray_url = (
        f"{TESTRAY_INSTANCE}/home/-/testray/case_results/{case_result_id}.json"
    )

    response = requests.request("GET", testray_url, auth=auth)

    return json.loads(response.text)


def get_relevant_jira_component(case_result, jira_connection, project_key):
    if project_key == "COMMERCE":
        return

    print("Matching the Jira component...")

    jira_components = get_project_components(jira_connection, project_key)

    jira_component_names = [jira_component.name for jira_component in jira_components]

    testray_component_name = get_case_component(case_result)

    components = [n for n in jira_component_names if testray_component_name in n]

    if len(components) == 0:
        if project_key == "LPS":
            components = ["Testing > Portal"]

        elif project_key == "LRAC":
            components = ["Test Infrastructure"]

    return components[0]


def main(assigned, case_result_id, label, project_key):
    testray_connection = get_testray_connection()

    case_result = get_case_result(testray_connection, case_result_id)

    case_name = get_case_name(case_result)

    case_error = get_case_error(case_result)

    jira_connection = get_jira_connection()

    component = get_relevant_jira_component(case_result, jira_connection, project_key)

    issue = add_test_fix_ticket(
        case_error, case_name, case_result_id, component, jira_connection, project_key
    )

    assign_to_me(assigned, jira_connection, issue)

    add_label(issue, label)

    print("Successful")

    print(f"{JIRA_INSTANCE}/browse/{issue.key}")
