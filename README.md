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

## Features

1. Create a pull request then forward

	1. Go to the `script` directory

        	python3 create_pr_and_forward.py

1. Forward a failure pull request to BrianChan

	1. Go to the `script` directory

        	python3 forward_failure_pull_request.py

1. Create a test fix ticket based on a given case result

	1. Go to the `script` directory

        	python3 create_test_fix_ticket.py

1. Write a comments template to a given jira ticket

	1. Go to the `script` directory

        	python3 write_comments.py

1. Write a description template to a given jira ticket

	1. Go to the `script` directory

        	python3 write_description.py
