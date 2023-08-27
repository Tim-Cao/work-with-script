def add_label(issue, label):
    if (label and not(label.isspace())):
        print("Adding label...")

        issue.fields.labels.append(label)
        issue.update(fields={"labels": issue.fields.labels})

def assign_to_me(assigned, jira_connection, issue):
    if assigned is True:
        print("Assigning...")

        issue.update(fields={'assignee': {'accountId': jira_connection.current_user()}})

def generate_comment(commit_id, description, env, type):
    match type:
        case "PID":
            return f"{{color:#36b37e}}*PASSED*{{color}} Manual Testing following the steps in the description.\n\n \
                    Fixed on:\n \
                    {env}. Portal master GIT ID: {commit_id}.\n\n \
                    {description}"
        case "FID":
            return f"{{color:#ff5630}}*FAILED*{{color}} Manual Testing following the steps in the description.\n\n \
                    Failed on:\n \
                    {env}. Portal master GIT ID: {commit_id}. \n\n \
                    {description}"
        case "NID":
            return f"{{color:#36b37e}}*No Longer Reproducible*{{color}} through Manual Testing following the steps in the description.\n\n \
                    No Longer Reproducible on:\n \
                    {env}. Portal master GIT ID: {commit_id}.\n\n \
                    {description}"
        case "PF":
            return f"{{color:#36b37e}}*PASSED*{{color}} Manual Testing using the following steps:\n\n#  \n#  \n#  \n\n \
                    Fixed on:\n \
                    {env}. Portal master GIT ID: {commit_id}.\n\n \
                    {description}"
        case "FF":
            return f"{{color:#ff5630}}*FAILED*{{color}} Manual Testing using the following steps:\n\n#  \n#  \n#  \n\n \
                    Failed on:\n \
                    {env}. Portal master GIT ID: {commit_id}.\n\n \
                    {description}"
        case "NF":
            return f"{{color:#36b37e}}*No Longer Reproducible*{{color}} through Manual Testing using the following steps:\n\n#  \n#  \n#  \n\n \
                    No Longer Reproducible on:\n \
                    {env}. Portal master GIT ID: {commit_id}.\n\n \
                    {description}"
        case "R":
            return f"(!) Reproduced on:\n \
                    {env}. Portal master GIT ID: {commit_id}."
        case "RU":
            return f"(!) Reproduced on:\n \
                    Upgrade From: 7.4.13-DXP-U60.\n \
                    {env}. Portal master GIT ID: {commit_id}."
        case "TV":
            return f"*Case 1:* Passed.\n \
                    *Case 2:* Passed.\n \
                    *Case 3:* Passed.\n\n \
                    *Tested on:*\n \
                    {env}. Portal master GIT ID: {commit_id}."
        
def generate_description(type):
    match type:
        case "STR":
            return "(on) *Steps to reproduce:*\n\n#  \n#  \n#  \n\n \
                    (/) *Expected Results:*\n\n \
                    (x) *Actual Results:*\n\n \
                    (!) Reproduced on:\n \
                    Tomcat 9.0.75 + MySQL. Portal master GIT ID: .\n\n \
                    (/) Cannot be Reproduced on:\n \
                    Tomcat 9.0.75 + MySQL. Portal 7.4.13-DXP-U89."
        case "TC":
            return "h3. *Test Cases*\n\n \
                    *Case 1:*\n \
                    The user can login after entering correct username and password.\n \
                    Test Strategy: CRITICAL\n \
                    Can be covered by POSHI?: Yes\n\n#  \n#  \n# \n\n \
                    *Case 2:*\n \
                    The user cannot login after entering wrong username and password.\n \
                    Test Strategy: HIGH\n \
                    Can be covered by POSHI?: Yes\n\n#  \n#  \n# \n\n \
                    *Case 3:*\n \
                    The user cannot login without entering password.\n \
                    Test Strategy: MEDIUM\n \
                    Can be covered by POSHI?: Yes\n\n#  \n#  \n# "

async def get_project_components(jira_connection, project_key):
    return await jira_connection.project_components(project_key)