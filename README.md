# Work with Script

## Installation

1. Clone this repository to a local directory

		git@github.com:Tim-Cao/work-with-script.git

## Configuration

1. Run the following command at the root directory of local repository

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

 1. Add a `credentials-ext.properties` file under the root directory to overwrite the `credentials.properties`

## Launch the app

1. Run the following command at the root directory of local repository

		python3 script_app.py

## Features

1. Create a pull request and forward

	![create_pr_and_forward](https://github.com/Tim-Cao/work-with-script/assets/52661397/6abf61fc-5182-4079-97cd-d4f2aa8d3f98)

1. Forward a failure pull request to BrianChan

	![forward_failure_pull_request](https://github.com/Tim-Cao/work-with-script/assets/52661397/c8228c98-5480-4ed0-9cac-f8842a5350a7)

1. Create a test fix ticket based on a given case result

	![create_test_fix_ticket](https://github.com/Tim-Cao/work-with-script/assets/52661397/6bd5dba6-5dc4-4003-80a9-8bf29ab3a9e3)

1. Write a comments template to a given jira ticket

	![write_comments](https://github.com/Tim-Cao/work-with-script/assets/52661397/64b6ef06-9967-4ac6-8b58-290c7af7f97b)

1. Write a description template to a given jira ticket

	![write_description](https://github.com/Tim-Cao/work-with-script/assets/52661397/714b4812-fdb2-4f61-9aeb-b7c024ea996b)