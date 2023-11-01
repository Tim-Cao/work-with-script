import os

from jproperties import Properties


def get_properties(product_team, key):
    configs = Properties()

    try:
        with open(
            os.path.join(os.path.dirname(__file__), "dependencies/")
            + "poshi_automation_"
            + product_team
            + ".properties",
            "rb",
        ) as config_file:
            configs.load(config_file)

        return configs.get(key).data
    except:
        pass


def get_components(key):
    configs = Properties()

    try:
        with open(
            os.path.join(os.path.dirname(__file__), "dependencies/")
            + "jira_components.properties",
            "rb",
        ) as config_file:
            configs.load(config_file)

        return configs.get(key).data
    except:
        pass


def add_label(issue, label):
    if label and not (label.isspace()):
        print("Adding label...")

        issue.fields.labels.append(label)
        issue.update(fields={"labels": issue.fields.labels})


def assign_to_me(assigned, jira_connection, issue):
    if assigned is True:
        print("Assigning...")

        issue.update(fields={"assignee": {"accountId": jira_connection.current_user()}})


def generate_comment(type):
    if type == "PID":
        return (
            "{color:#36b37e}*PASSED*{color} Manual Testing following the steps in the description.\n\n"
            + "Fixed on:\n"
            + "Tomcat 9.0.82 + MySQL. Portal master GIT ID: .\n\n"
        )
    elif type == "FID":
        return (
            "{color:#ff5630}*FAILED*{color} Manual Testing following the steps in the description.\n\n"
            + "Failed on:\n"
            + "Tomcat 9.0.82 + MySQL. Portal master GIT ID: .\n\n"
        )
    elif type == "NID":
        return (
            "{color:#36b37e}*No Longer Reproducible*{color} through Manual Testing following the steps in the description.\n\n"
            + "No Longer Reproducible on:\n"
            + "Tomcat 9.0.82 + MySQL. Portal master GIT ID: .\n\n"
        )
    elif type == "PF":
        return (
            "{color:#36b37e}*PASSED*{color} Manual Testing using the following steps:\n"
            + "# \n# \n# \n\n"
            + "Fixed on:\n"
            + "Tomcat 9.0.82 + MySQL. Portal master GIT ID: .\n\n"
        )
    elif type == "FF":
        return (
            "{color:#ff5630}*FAILED*{color} Manual Testing using the following steps:\n"
            + "# \n# \n# \n\n"
            + "Failed on:\n"
            + "Tomcat 9.0.82 + MySQL. Portal master GIT ID: .\n\n"
        )
    elif type == "NF":
        return (
            "{color:#36b37e}*No Longer Reproducible*{color} through Manual Testing using the following steps:\n"
            + "# \n# \n# \n\n"
            + "No Longer Reproducible on:\n"
            + "Tomcat 9.0.82 + MySQL. Portal master GIT ID: .\n\n"
        )
    elif type == "R":
        return "(!) Reproduced on:\n" + "Tomcat 9.0.82 + MySQL. Portal master GIT ID: ."
    elif type == "RU":
        return (
            "(!) Reproduced on:\n"
            + "Upgrade From: 7.4.13-DXP-U60.\n"
            + "Tomcat 9.0.82 + MySQL. Portal master GIT ID: ."
        )
    elif type == "TV":
        return (
            "*Case 1:* Passed.\n"
            + "*Case 2:* Passed.\n"
            + "*Case 3:* Passed.\n\n"
            + "*Tested on:*\n"
            + "Tomcat 9.0.82 + MySQL. Portal master GIT ID: ."
        )


def generate_description(type):
    if type == "Default":
        return (
            "(on) *Steps to reproduce:*\n"
            + "# \n# \n# \n# \n# \n\n"
            + "(/) *Expected Results:*\n\n\n"
            + "(x) *Actual Results:*\n\n\n"
            + "(!) Reproduced on:\n"
            + "Tomcat 9.0.82 + MySQL. Portal master GIT ID: .\n\n"
        )
    elif type == "Regression Bug":
        return (
            "(on) *Steps to reproduce:*\n"
            + "# \n# \n# \n# \n# \n\n"
            + "(/) *Expected Results:*\n\n\n"
            + "(x) *Actual Results:*\n\n\n"
            + "(!) Reproduced on:\n"
            + "Tomcat 9.0.82 + MySQL. Portal master GIT ID: .\n\n"
            + "(/) Cannot be Reproduced on:\n"
            + "Tomcat 9.0.82 + MySQL. Portal 7.4.13-DXP-U100."
        )
    elif type == "STR":
        return (
            "(on) *Steps to reproduce:*\n"
            + "# \n# \n# \n# \n# \n\n"
            + "(/) *Expected Results:*\n\n\n"
            + "(x) *Actual Results:*\n\n\n"
            + "(!) Reproduced on:\n"
            + "Tomcat 9.0.82 + MySQL. Portal master GIT ID: .\n\n"
            + "(/) Cannot be Reproduced on:\n"
            + "Tomcat 9.0.82 + MySQL. Portal 7.4.13-DXP-U100."
        )
    elif type == "TC":
        return (
            "h3.*Test Cases*\n"
            + "*Case 1:*\n"
            + "The user can login after entering correct username and password.\n"
            + "Test Strategy: CRITICAL\n"
            + "Can be covered by POSHI?: Yes\n"
            + "# \n# \n# \n\n"
            + "*Case 2:*\n"
            + "The user cannot login after entering wrong username and password.\n"
            + "Test Strategy: HIGH\n"
            + "Can be covered by POSHI?: Yes\n"
            + "# \n# \n# \n\n"
            + "*Case 3:*\n"
            + "The user cannot login without entering password.\n"
            + "Test Strategy: MEDIUM\n"
            + "Can be covered by POSHI?: Yes\n"
            + "# \n# \n# "
        )


def get_project_components(jira_connection, project_key):
    return jira_connection.project_components(project_key)
