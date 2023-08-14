# Script to create test fix ticket based on a given case result

import json
import os
import sys

import requests
from jsonpath_ng.ext import parse

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from liferay.jira.jira_connection import get_jira_connection
from liferay.jira.jira_constants import *
from liferay.jira.jira_util import *
from liferay.testray.testray_connection import get_testray_connection
from liferay.testray.testray_constants import *
from liferay.util.credentials import get_credentials


def add_test_fix_ticket(jira_connection, component, case_name, case_error):
    issue_dict = {
        'project': {'key': 'LPS'},
        'summary': 'Investigate failure in ' + case_name,
        'description': '*Error Message*\n\n{code:java}' + case_error + \
                        '{code}\n\n*Affect Tests*\n[' + case_name + '|' + \
                        TESTRAY_INSTANCE + '/home/-/testray/case_results/' + \
                        case_result_id + ']',
        'components': [{'name': component}],
        'issuetype': {'name': 'Testing'},
        'customfield_10383': {'value': 'Analysis'}
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
    testray_url = TESTRAY_INSTANCE + "/home/-/testray/case_results/" + case_result_id + ".json"

    response = requests.request("GET", testray_url, auth=auth)

    return json.loads(response.text)

def get_relevant_jira_component(jira_connection, case_result):
    jira_components = get_project_components(jira_connection, get_credentials("PROJECT_KEY"))

    jira_component_names = [jira_component.name for jira_component in jira_components]

    testray_component_name = get_case_component(case_result)

    components = [n for n in jira_component_names if testray_component_name in n]

    if len(components) == 0:
        components = ['Testing > Portal']

    return components[0]

if __name__ == "__main__":
    testray_connection = get_testray_connection()

    case_result = get_case_result(testray_connection, input("Enter the case result id: "))

    case_name = get_case_name(case_result)

    case_error = get_case_error(case_result)

    jira_connection = get_jira_connection()

    component = get_relevant_jira_component(jira_connection, case_result)

    issue = add_test_fix_ticket(jira_connection, component, case_name, case_error)

    assign_to_me(jira_connection, issue)

    add_label(issue)

    print(JIRA_INSTANCE + "/browse/" + str(issue))