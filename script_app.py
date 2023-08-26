import os
import sys

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import *
from textual.widgets import *

root = os.path.dirname(__file__)

sys.path.append(root)

from liferay.apps import (create_pr_and_forward, create_test_fix_ticket,
                          forward_failure_pull_request, write_comments,
                          write_description)


class ScriptApp(App):
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("shift+insert", "paste", "Paste"),
        Binding("ctrl+u", "delete_left_all", "Delete all to the left")
    ]

    CSS_PATH = root + "/liferay/src/css/main.css"

    TITLE = "Working with Script"

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield ListView(
                ListItem(Static("Forward Failure PR", classes="nav-item"), id="nav-1"),
                ListItem(Static("Create PR And Forward", classes="nav-item"), id="nav-2"),
                ListItem(Static("Create TF Ticket", classes="nav-item"), id="nav-3"),
                ListItem(Static("Write Comments", classes="nav-item"), id="nav-4"),
                ListItem(Static("Write Description", classes="nav-item"), id="nav-5")
            )
            with ContentSwitcher(initial="nav-1"):
                with Vertical(id="nav-1"):
                    yield Label("Enter the failure Pull Request Number: ")
                    yield Input(id='failure-pull-request-number')
                    yield Static()
                    yield Button("Submit", variant="primary", id='button-1')
                with Vertical(id="nav-2"):
                    yield Label("Local Branch Name: ")
                    yield Input(id='local-branch')
                    yield Label("Jira Ticket Number: ")
                    yield Input(id='jira-ticket-number-2')
                    yield Static()
                    yield Button("Submit", variant="primary", id='button-2')
                with Vertical(id="nav-3"):
                    PROJECT_KEY = [
                        ("LPS", "LPS"),
                        ("LRQA", "LRQA"),
                        ("LRAC", "LRAC"),
                        ("COMMERCE", "COMMERCE")
                    ]

                    yield Label("Enter the Case Result Id: ")
                    yield Input(id='case-result-id')
                    yield Label("Select the Project Key: ")
                    yield Select(PROJECT_KEY, id='project-key', value="LPS")
                    yield Static()
                    with Horizontal(id='switch-container'):
                        yield Switch(id='assign-to-me', value=False)
                        yield Static("Assign to me (Optional)", id='assign-to-me-label')
                    yield Label("Add label (Optional)")
                    yield Input(id='add-label')
                    yield Static()
                    yield Button("Submit", variant="primary", id='button-3')
                with Vertical(id="nav-4"):
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

                    yield Label("Jira Ticket Number: ")
                    yield Input(id='jira-ticket-number-4')
                    yield Label("Select the Comments Type: ")
                    yield Select(COMMENTS_TYPE, id="comments-type")
                    yield Label("Enter the environment: (e.g., Tomcat 9.0.75 + MySQL)")
                    yield Input(id='env', value="Tomcat 9.0.75 + MySQL")
                    yield Label("Enter the commit id: (Optional)")
                    yield Input(id='commit-id')
                    yield Label("Enter the description: (Optional)")
                    yield Input(id='description')
                    yield Static()
                    yield Button("Submit", variant="primary", id='button-4')
                with Vertical(id="nav-5"):
                    DESCRIPTION_TYPE = [
                        ("Steps to reproduce", "STR"),
                        ("Test Cases", "TC")
                    ]

                    yield Label("Jira Ticket Number: ")
                    yield Input(id='jira-ticket-number-5')
                    yield Label("Select the Description Type: ")
                    yield Select(DESCRIPTION_TYPE, id='description-type')
                    yield Static()
                    yield Button("Submit", variant="primary", id='button-5')
        yield VerticalScroll(id="output")
        yield Footer()

    def create_pr_and_forward(self) -> None:
        local_branch_name= self.query_one("#local-branch").value
        jira_ticket_number= self.query_one("#jira-ticket-number-2").value

        link = create_pr_and_forward.main(local_branch_name, jira_ticket_number)

        self.query_one(VerticalScroll).mount(Label(f"{link}"))

    def create_test_fix_ticket(self) -> None:
        assigned = self.query_one("#assign-to-me").value
        case_result_id = self.query_one("#case-result-id").value
        label = self.query_one("#add-label").value
        project_key = self.query_one("#project-key").value

        link = create_test_fix_ticket.main(assigned, case_result_id, label, project_key)

        self.query_one(VerticalScroll).mount(Label(f"{link}"))

    def forward_failure_pull_request(self) -> None:
        failure_pull_request_number = self.query_one("#failure-pull-request-number").value

        link = forward_failure_pull_request.main(failure_pull_request_number)

        self.query_one(VerticalScroll).mount(Label(f"{link}"))

    def write_comments(self) -> None:
        commit_id = self.query_one("#commit-id").value
        description = self.query_one("#description").value
        env = self.query_one("#env").value
        ticket_number = self.query_one("#jira-ticket-number-4").value
        type = self.query_one("#comments-type").value

        link = write_comments.main(commit_id, description, env, ticket_number, type)

        self.query_one(VerticalScroll).mount(Label(f"{link}"))

    def write_description(self) -> None:
        ticket_number = self.query_one("#jira-ticket-number-5").value
        type = self.query_one("#description-type").value

        link = write_description.main(ticket_number, type)

        self.query_one(VerticalScroll).mount(Label(f"{link}"))

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

app = ScriptApp()

if __name__ == "__main__":
    app.run()