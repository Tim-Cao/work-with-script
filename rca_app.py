import os
import sys

from textual import on, work
from textual.app import App, ComposeResult, events
from textual.binding import Binding
from textual.containers import *
from textual.widgets import *

root = os.path.dirname(__file__)

sys.path.append(root)

from liferay.csv import convert_commits_to_tickets
from liferay.git.git_util import *
from liferay.git.github_connection import *
from liferay.jira.jira_constants import *
from liferay.util import credentials


class ScriptApp(App):
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("shift+insert", "paste", "Paste text from the clipboard"),
        Binding("ctrl+o", "open_credentials", "Open the credentials-ext.properties"),
    ]

    CSS_PATH = root + "/liferay/src/css/main.css"

    TITLE = "Working with Script"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Enter the repo name: ")
        yield Input(id="repo-name", value="liferay/liferay-portal")
        yield Label("Enter the last pass sha: ")
        yield Input(id="base")
        yield Label("Enter the first failure sha: ")
        yield Input(id="head")
        yield Static()
        yield Button("Submit", variant="primary", id="button-1")
        yield Output(highlight=True, markup=True)
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "button-1":
            self.conversion()

    @work(exclusive=True, thread=True)
    def conversion(self) -> None:
        baseSHA = self.query_one("#base").value
        headSHA = self.query_one("#head").value
        repo_name = self.query_one("#repo-name").value

        self.query_one("#button-1").disabled = True

        self.query_one(RichLog).clear()
        self.query_one(RichLog).begin_capture_print()

        convert_commits_to_tickets.main(baseSHA, headSHA, repo_name)

        self.query_one("#button-1").disabled = False
        self.query_one("#base").value = ""
        self.query_one("#head").value = ""
        self.query_one("#repo-name").value = "liferay/liferay-portal"

    @work(exclusive=True, thread=True)
    def action_open_credentials(self) -> None:
        self.query_one(RichLog).clear()
        self.query_one(RichLog).begin_capture_print()

        credentials.open_credentials()


class Output(RichLog):
    @on(events.Print)
    def on_print(self, event: events.Print) -> None:
        if event.text.strip():
            self.write(event.text)


app = ScriptApp()

if __name__ == "__main__":
    app.run()
