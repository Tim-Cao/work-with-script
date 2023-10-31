# Work with Script

## Requirements

1. Python 3.9 or above

1. python3-pip

## Installation

1. Clone this repository to a local directory

		git@github.com:Tim-Cao/work-with-script.git

## Configuration

1. Run the following command at the root directory of local repository, it will generate a `credentials-ext.properties`

		python3 initialization.py

1. Generate jira API Token

	1. Sign in https://liferay.atlassian.net/

	1. Click the cog icon > Atlassian account settings > Security > Create and manage API tokens

	1. Create API Token

	1. Save generated token in your local file as you will not be able to see this again.

1. Generate github API Token

	1. Sign in https://github.com/

	1. Personal Menu > Settings > Developer Settings > Personal access tokens > Tokens(classic)  > Generate new token

	1. Add a name > Leave expiration as default > Select the following scopes

		![image](https://github.com/Tim-Cao/work-with-script/assets/52661397/3478cd82-4e48-4306-99a1-fab363498b24)

		![image](https://github.com/Tim-Cao/work-with-script/assets/52661397/68c7945c-ef1c-47d6-a8ad-a14d7f5d8922)

	1. Generate token

	1. Save generated token in your local file as you will not be able to see this again.

1. Please fill out the value of properties in the `credentials-ext.properties`

	1. For required properties of each feature, please see [Features](#Features) section

## Upgrade dependencies

1. Run the following command at the root directory of local repository

		python3 upgrade.py

## Launch the app

1. Run the following command at the root directory of local repository

		python3 script_app.py

## Open the credentials-ext.properties

1. Execute `ctrl + o` shortcuts in app

	1. This file will open with vscode automatically.

	1. If you don't install vscode. Please open it manually.

## See more shortcuts

1. Execute `ctrl + b` shortcuts in app

	1. All shortcuts details will appear on a sidebar.

## Features

1. Create a pull request and forward

	![create_pr_and_forward](https://github.com/Tim-Cao/work-with-script/assets/52661397/c5098644-371f-4f02-9cad-6db868dba901)

	See pull request [styles](https://liferay.atlassian.net/wiki/spaces/QA/pages/2194800714/Script+to+manual+forward+PR+to+Brian#Styles)

	Required properties: `GITHUB_REVIEWER_NAME`, `GITHUB_USER_NAME`, `GITHUB_TOKEN`, `LOCAL_REPO_PATH`, `TEAM_REPO_NAME`

1. Forward a failure pull request to BrianChan

	![forward_failure_pull_request](https://github.com/Tim-Cao/work-with-script/assets/52661397/cb298653-f9ba-485a-982f-9a14d1dac260)

	See pull request [styles](https://liferay.atlassian.net/wiki/spaces/~292455967/pages/2421522433/Script+to+create+a+PR+with+only+Poshi+changes+to+team+repo+then+forward#Styles)

	Required properties: `GITHUB_USER_NAME`, `GITHUB_TOKEN`, `LOCAL_REPO_PATH`, `TEAM_REPO_NAME`

1. Create a test fix ticket based on a given case result

	![create_test_fix_ticket](https://github.com/Tim-Cao/work-with-script/assets/52661397/b69c0165-1a41-4625-a263-de77e5dba11e)

	Required properties: `JIRA_USER_NAME`, `JIRA_TOKEN`, `TESTRAY_USER_NAME`, `TESTRAY_PASSWORD`

1. Write a comments template to a given jira ticket

	![write_comments](https://github.com/Tim-Cao/work-with-script/assets/52661397/19596826-52ab-4b4f-8e53-7a3c0ecdb580)

	See comments [styles](https://liferay.atlassian.net/wiki/spaces/~292455967/pages/2402025586/Ticket+description+and+comments+template+on+Jira+Software+Cloud#Comments)

	Required properties: `JIRA_USER_NAME`, `JIRA_TOKEN`

1. Write a description template to a given jira ticket

	![write_description](https://github.com/Tim-Cao/work-with-script/assets/52661397/1ed9938f-2f09-4052-a328-762d4c7915c4)

	See description [styles](https://liferay.atlassian.net/wiki/spaces/~292455967/pages/2402025586/Ticket+description+and+comments+template+on+Jira+Software+Cloud#Description)

	Required properties: `JIRA_USER_NAME`, `JIRA_TOKEN`

1. Trigger gauntlet test suite on ci

	![Trigger_Gauntlet](https://github.com/Tim-Cao/work-with-script/assets/52661397/1c6cae50-005e-4463-aecb-9fe295513284)

	Required properties: `JIRA_USER_NAME`, `JIRA_TOKEN`, `LEGACY_REPO_PATH`, `GITHUB_USER_NAME`, `GITHUB_TOKEN`
