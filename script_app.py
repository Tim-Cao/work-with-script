import os
import sys

from textual import on, work
from textual.app import App, ComposeResult, events
from textual.binding import Binding
from textual.containers import *
from textual.widgets import *

root = os.path.dirname(__file__)

sys.path.append(root)

from liferay.apps import (create_pr_and_forward, create_test_fix_ticket,
                          forward_failure_pull_request, write_comments,
                          write_description)
from liferay.util import credentials


class ScriptApp(App):
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("shift+insert", "paste", "Paste"),
        Binding("ctrl+u", "delete_left_all", "Delete all to the left"),
        Binding("ctrl+o", "open_credentials", "Open credentials-ext")
    ]

    CSS_PATH = root + "/liferay/src/css/main.css"

    TITLE = "Working with Script"

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id='main-content'):
            yield ListView(
                ListItem(Static("Forward Failure PR", classes="nav-item"), id="nav-1"),
                ListItem(Static("Create PR and Forward", classes="nav-item"), id="nav-2"),
                ListItem(Static("Create TF Ticket", classes="nav-item"), id="nav-3"),
                ListItem(Static("Write Comments", classes="nav-item"), id="nav-4"),
                ListItem(Static("Write Description", classes="nav-item"), id="nav-5")
            )
            with ContentSwitcher(initial="nav-1"):
                with VerticalScroll(id="nav-1"):
                    yield Label("Enter the failure pull request number: ")
                    yield Input(id='failure-pull-request-number')
                    yield Static()
                    yield Button("Submit", variant="primary", id='button-1')
                with VerticalScroll(id="nav-2"):
                    yield Label("Enter the local branch name: ")
                    yield Input(id='local-branch')
                    yield Label("Enter the Jira ticket number: ")
                    yield Input(id='jira-ticket-number-2')
                    yield Static()
                    yield Button("Submit", variant="primary", id='button-2')
                with VerticalScroll(id="nav-3"):
                    PROJECT_KEY = [
                        ("LPS", "LPS"),
                        ("LRQA", "LRQA"),
                        ("LRAC", "LRAC"),
                        ("COMMERCE", "COMMERCE")
                    ]

                    yield Label("Enter the case result id: ")
                    yield Input(id='case-result-id')
                    yield Label("Select the project key: ")
                    yield Select(PROJECT_KEY, id='project-key', value="LPS")
                    yield Static()
                    with Horizontal(id='switch-container'):
                        yield Switch(id='assign-to-me', value=False)
                        yield Static("Assign to me (Optional)", id='assign-to-me-label')
                    yield Label("Add label (Optional)")
                    yield Input(id='add-label')
                    yield Static()
                    yield Button("Submit", variant="primary", id='button-3')
                with VerticalScroll(id="nav-4"):
                    COMMENTS_TYPE = [
                        ("PASSED Manual Testing following the steps in the description.", "PID"),
                        ("FAILED Manual Testing following the steps in the description.", "FID"),
                        ("No Longer Reproducible through Manual Testing following the steps in the description.", "NID"),
                        ("PASSED Manual Testing using the following steps:", "PF"),
                        ("FAILED Manual Testing using the following steps:", "FF"),
                        ("No Longer Reproducible through Manual Testing using the following steps:", "NF"),
                        ("Reproduced on:", "R"),
                        ("Reproduced on: Upgrade From:", "RU"),
                        ("Test Validation", "TV")
                    ]

                    yield Label("Enter the Jira ticket number: ")
                    yield Input(id='jira-ticket-number-4')
                    yield Label("Select the comments type: ")
                    yield Select(COMMENTS_TYPE, id="comments-type")
                    yield Label("Enter the environment: (e.g., Tomcat 9.0.80 + MySQL)")
                    yield Input(id='env', value="Tomcat 9.0.80 + MySQL")
                    yield Label("Enter the commit id: (Optional)")
                    yield Input(id='commit-id')
                    yield Label("Enter the description: (Optional)")
                    yield Input(id='description')
                    yield Static()
                    yield Button("Submit", variant="primary", id='button-4')
                with VerticalScroll(id="nav-5"):
                    DESCRIPTION_TYPE = [
                        ("Steps to reproduce", "STR"),
                        ("Test Cases", "TC")
                    ]

                    yield Label("Enter the Jira ticket number: ")
                    yield Input(id='jira-ticket-number-5')
                    yield Label("Select the description type: ")
                    yield Select(DESCRIPTION_TYPE, id='description-type')
                    yield Static()
                    yield Button("Submit", variant="primary", id='button-5')
        yield Output(highlight=True, markup=True)
        yield Footer()

    @work(exclusive=True, thread=True)
    def action_open_credentials(self) -> None:
        self.query_one(RichLog).clear()
        self.query_one(RichLog).begin_capture_print()

        credentials.open_credentials()

    @work(exclusive=True, thread=True)
    def create_pr_and_forward(self) -> None:
        local_branch_name= self.query_one("#local-branch").value
        jira_ticket_number= self.query_one("#jira-ticket-number-2").value

        self.query_one("#button-2").disabled = True

        self.query_one(RichLog).clear()
        self.query_one(RichLog).begin_capture_print()

        create_pr_and_forward.main(local_branch_name, jira_ticket_number)

        self.query_one("#button-2").disabled = False
        self.query_one("#local-branch").value = ""
        self.query_one("#jira-ticket-number-2").value = ""

    @work(exclusive=True, thread=True)
    def create_test_fix_ticket(self) -> None:
        assigned = self.query_one("#assign-to-me").value
        case_result_id = self.query_one("#case-result-id").value
        label = self.query_one("#add-label").value
        project_key = self.query_one("#project-key").value

        self.query_one("#button-3").disabled = True

        self.query_one(RichLog).clear()
        self.query_one(RichLog).begin_capture_print()

        create_test_fix_ticket.main(assigned, case_result_id, label, project_key)

        self.query_one("#button-3").disabled = False
        self.query_one("#assign-to-me").value = False
        self.query_one("#case-result-id").value = ""
        self.query_one("#add-label").value = ""
        self.query_one("#project-key").value = "LPS"

    @work(exclusive=True, thread=True)
    def forward_failure_pull_request(self) -> None:
        failure_pull_request_number = self.query_one("#failure-pull-request-number").value

        self.query_one("#button-1").disabled = True

        self.query_one(RichLog).clear()
        self.query_one(RichLog).begin_capture_print()

        forward_failure_pull_request.main(failure_pull_request_number)

        self.query_one("#button-1").disabled = False
        self.query_one("#failure-pull-request-number").value = ""

    @work(exclusive=True, thread=True)
    def write_comments(self) -> None:
        commit_id = self.query_one("#commit-id").value
        description = self.query_one("#description").value
        env = self.query_one("#env").value
        ticket_number = self.query_one("#jira-ticket-number-4").value
        type = self.query_one("#comments-type").value

        self.query_one("#button-4").disabled = True

        self.query_one(RichLog).clear()
        self.query_one(RichLog).begin_capture_print()

        write_comments.main(commit_id, description, env, ticket_number, type)

        self.query_one("#button-4").disabled = False
        self.query_one("#commit-id").value = ""
        self.query_one("#description").value = ""
        self.query_one("#env").value = "Tomcat 9.0.80 + MySQL"
        self.query_one("#jira-ticket-number-4").value = ""
        self.query_one("#comments-type").value = ""

    @work(exclusive=True, thread=True)
    def write_description(self) -> None:
        ticket_number = self.query_one("#jira-ticket-number-5").value
        type = self.query_one("#description-type").value

        self.query_one("#button-5").disabled = True

        self.query_one(RichLog).clear()
        self.query_one(RichLog).begin_capture_print()

        write_description.main(ticket_number, type)

        self.query_one("#button-5").disabled = False
        self.query_one("#jira-ticket-number-5").value = ""
        self.query_one("#description-type").value = ""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "button-1":
            self.forward_failure_pull_request()
        elif event.button.id == "button-2":
            self.create_pr_and_forward()
        elif event.button.id == "button-3":
            self.create_test_fix_ticket()
        elif event.button.id == "button-4":
            self.write_comments()
        elif event.button.id == "button-5":
            self.write_description()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        self.query_one(ContentSwitcher).current = event.item.id

class Output(RichLog):
    @on(events.Print)
    def on_print(self, event: events.Print) -> None:
        if event.text.strip():
            self.write(event.text)

app = ScriptApp()

if __name__ == "__main__":
    app.run()