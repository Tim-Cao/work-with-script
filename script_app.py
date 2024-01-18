import json
import os
import sys
import webbrowser

from git.exc import GitCommandError
from jira.exceptions import JIRAError
from textual import on, work
from textual.app import App, ComposeResult, events
from textual.binding import Binding
from textual.containers import *
from textual.reactive import reactive
from textual.widgets import *

root = os.path.dirname(__file__)

sys.path.append(root)

from liferay.apps import (
    create_issue,
    create_pr_and_forward,
    create_test_fix_ticket,
    forward_failure_pull_request,
    trigger_gauntlet,
    write_comments,
    write_description,
)
from liferay.csv import convert_commits_to_tickets
from liferay.jira import jira_components_sync
from liferay.jira.jira_constants import *
from liferay.jira.jira_util import *
from liferay.util import credentials
from widgets.form import *
from widgets.menubar import *
from widgets.output import *
from widgets.sidebar import *
from widgets.submit import *
from widgets.text_field import *
from widgets.textarea_field import *
from widgets.toggle_switch import *


class ScriptApp(App):
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("ctrl+b", "toggle_sidebar", "More Shortcuts"),
        Binding("shift+insert", "paste", show=False),
        Binding("ctrl+u", "delete_left_all", show=False),
        Binding("ctrl+o", "open_credentials", show=False),
        Binding("ctrl+s", "sync_components", show=False),
    ]

    CSS_PATH = root + "/liferay/src/css/main.css"

    TITLE = "Working with Script"

    show_sidebar = reactive(False)

    def compose(self) -> ComposeResult:
        yield Sidebar(classes="-hidden")
        yield Header()
        with Horizontal(id="main-content"):
            yield Menubar(
                MenuItem("Forward Failure PR", "nav-1"),
                MenuItem("Create PR and Forward", "nav-2"),
                MenuItem("Create TF Ticket", "nav-3"),
                MenuItem("Write Comments", "nav-4"),
                MenuItem("Write Description", "nav-5"),
                MenuItem("Trigger Gauntlet", "nav-6"),
                MenuItem("Create Issue", "nav-7"),
                MenuItem("RCA", "nav-8"),
            )
            with ContentSwitcher(initial="nav-1"):
                with Form("nav-1"):
                    yield TextField(
                        "Enter the failure pull request number: ",
                        "failure-pull-request-number",
                    )
                    yield Submit("button-1")
                with Form("nav-2"):
                    yield TextField("Enter the local branch name: ", "local-branch")
                    yield TextField(
                        "Enter the Jira ticket number: ", "jira-ticket-number-2"
                    )
                    yield Submit("button-2")
                with Form("nav-3"):
                    PROJECT_KEY = [
                        ("LPS", "LPS"),
                        ("LRQA", "LRQA"),
                        ("LRAC", "LRAC"),
                        ("COMMERCE", "COMMERCE"),
                    ]

                    yield TextField("Enter the case result id: ", "case-result-id")
                    yield Label("Select the project key: ")
                    yield Select(PROJECT_KEY, id="project-key-1", value="LPS")
                    yield ToggleSwitch("assign-to-me-1")
                    yield TextField("Add label (Optional)", "add-label")
                    yield Submit("button-3")
                with Form("nav-4"):
                    COMMENTS_TYPE = [
                        (
                            "PASSED Manual Testing following the steps in the description.",
                            "PID",
                        ),
                        (
                            "FAILED Manual Testing following the steps in the description.",
                            "FID",
                        ),
                        (
                            "No Longer Reproducible through Manual Testing following the steps in the description.",
                            "NID",
                        ),
                        ("PASSED Manual Testing using the following steps:", "PF"),
                        ("FAILED Manual Testing using the following steps:", "FF"),
                        (
                            "No Longer Reproducible through Manual Testing using the following steps:",
                            "NF",
                        ),
                        ("Reproduced on:", "R"),
                        ("Reproduced on: Upgrade From:", "RU"),
                        ("Test Validation", "TV"),
                    ]

                    yield TextField(
                        "Enter the Jira ticket number: ", "jira-ticket-number-4"
                    )
                    yield Label("Select the comments type: ")
                    yield Select(COMMENTS_TYPE, id="comments-type")
                    yield TextAreaField(
                        "Enter the comments: ", "comments", "unselected"
                    )
                    yield Submit("button-4")
                with Form("nav-5"):
                    DESCRIPTION_TYPE = [
                        ("Steps to reproduce", "STR"),
                        ("Test Cases", "TC"),
                    ]

                    yield TextField(
                        "Enter the Jira ticket number: ", "jira-ticket-number-5"
                    )
                    yield Label("Select the description type: ")
                    yield Select(DESCRIPTION_TYPE, id="description-type")
                    yield TextAreaField(
                        "Enter the description: ", "description", "unselected"
                    )
                    yield Submit("button-5")
                with Form("nav-6"):
                    yield TextField(
                        "Enter the legacy repo path: ",
                        "legacy-repo-path",
                        value=credentials.get_credentials("LEGACY_REPO_PATH"),
                    )
                    yield TextField(
                        "Enter the target branch: ", "target-branch", value="7.3.x"
                    )
                    yield Submit("button-6")
                with Form("nav-7"):
                    PROJECT_KEY = [
                        ("LPS", "LPS"),
                        ("LRQA", "LRQA"),
                        ("LRAC", "LRAC"),
                        ("COMMERCE", "COMMERCE"),
                    ]

                    PRODUCT_TEAM = [
                        ("Business Process Management Team", "bpm"),
                    ]

                    ISSUE_TYPE = [
                        ("Bug", "Bug"),
                        ("Task", "Task"),
                    ]

                    BUG_TYPE = [
                        ("Default", "Default"),
                        ("Regression Bug", "Regression Bug"),
                    ]

                    yield Label("Project Key:", id="project-key-label-2")
                    yield Select(PROJECT_KEY, id="project-key-2")
                    yield Label("Issue Type:", id="issue-type-label")
                    yield Select(ISSUE_TYPE, id="issue-type")
                    yield Label("Bug Type:", id="bug-type-label", classes="unselected")
                    yield Select(BUG_TYPE, id="bug-type", classes="unselected")
                    yield Label(
                        "Product Team:", id="product-team-label", classes="unselected"
                    )
                    yield Select(PRODUCT_TEAM, id="product-team", classes="unselected")
                    yield TextField("Summary:", "summary", "unselected")
                    yield Label(
                        "Components:", id="components-label", classes="unselected"
                    )
                    yield Select([], id="components", classes="unselected")
                    yield TextField(
                        "Affects versions:",
                        "affects-versions",
                        "unselected",
                        value="Master",
                    )
                    yield TextAreaField(
                        "Description:", "issue-description", "unselected"
                    )
                    yield ToggleSwitch("assign-to-me-2")
                    yield TextField("Add label (Optional)", "issue-label")
                    yield Submit("button-7")
                with Form("nav-8"):
                    yield TextField(
                        "Enter the repo name: ",
                        "repo-name",
                        value="liferay/liferay-portal",
                    )
                    yield TextField("Enter the last pass sha: ", "base")
                    yield TextField("Enter the first failure sha: ", "head")
                    yield Submit("button-8")
        yield Output(highlight=True, markup=True)
        yield Footer()

    @work(exclusive=True, thread=True)
    def action_open_credentials(self) -> None:
        self.query_one(RichLog).clear()
        self.query_one(RichLog).begin_capture_print()

        credentials.open_credentials()

    @work(exclusive=True, thread=True)
    def action_sync_components(self) -> None:
        self.query_one(RichLog).clear()
        self.query_one(RichLog).begin_capture_print()

        jira_components_sync.main()

    @work(exclusive=True, thread=True)
    def action_toggle_sidebar(self) -> None:
        sidebar = self.query_one(Sidebar)
        self.set_focus(None)
        if sidebar.has_class("-hidden"):
            self.call_from_thread(sidebar.remove_class, "-hidden")
        else:
            if sidebar.query("*:focus"):
                self.screen.set_focus(None)
            self.call_from_thread(sidebar.add_class, "-hidden")

    @work(exclusive=True, thread=True)
    def create_pr_and_forward(self) -> None:
        local_branch_name = self.query_one("#local-branch").value
        jira_ticket_number = self.query_one("#jira-ticket-number-2").value

        self.query_one("#button-2").disabled = True

        self.query_one(RichLog).clear()
        self.query_one(RichLog).begin_capture_print()

        try:
            create_pr_and_forward.main(local_branch_name, jira_ticket_number)

            self.query_one("#button-2").disabled = False
            self.query_one("#local-branch").value = ""
            self.query_one("#jira-ticket-number-2").value = ""
        except (AssertionError, JIRAError, GitCommandError):
            print(
                f"\033[1;31mPlease check your credentials in credentials-ext.properties\033[0m"
            )
        finally:
            self.query_one("#button-2").disabled = False

    @work(exclusive=True, thread=True)
    def create_test_fix_ticket(self) -> None:
        assigned = self.query_one("#assign-to-me-1").value
        case_result_id = self.query_one("#case-result-id").value
        label = self.query_one("#add-label").value
        project_key = self.query_one("#project-key-1").value

        self.query_one("#button-3").disabled = True

        self.query_one(RichLog).clear()
        self.query_one(RichLog).begin_capture_print()

        try:
            create_test_fix_ticket.main(assigned, case_result_id, label, project_key)

            self.query_one("#button-3").disabled = False
            self.query_one("#assign-to-me-1").value = False
            self.query_one("#case-result-id").value = ""
            self.query_one("#add-label").value = ""
            self.query_one("#project-key-1").value = "LPS"
        except (AssertionError, JIRAError, json.decoder.JSONDecodeError):
            print(
                f"\033[1;31mPlease check your credentials in credentials-ext.properties\033[0m"
            )
        finally:
            self.query_one("#button-3").disabled = False

    @work(exclusive=True, thread=True)
    def create_issue(self) -> None:
        affects_versions = self.query_one("#affects-versions").value
        assigned = self.query_one("#assign-to-me-2").value
        bug_type = self.query_one("#bug-type").value
        component = self.query_one("#components").value
        description = self.query_one("#issue-description").text
        issue_type = self.query_one("#issue-type").value
        label = self.query_one("#issue-label").value
        project_key = self.query_one("#project-key-2").value
        summary = self.query_one("#summary").value
        self.query_one("#button-7").disabled = True

        self.query_one(RichLog).clear()
        self.query_one(RichLog).begin_capture_print()

        try:
            create_issue.main(
                affects_versions,
                assigned,
                bug_type,
                component,
                description,
                issue_type,
                label,
                project_key,
                summary,
            )

            self.query_one("#affects-versions").value = "Master"
            self.query_one("#assign-to-me-2").value = False
            self.query_one("#bug-type").clear()
            self.query_one("#components").clear()
            self.query_one("#issue-type").clear()
            self.query_one("#issue-label").value = ""
            self.query_one("#summary").value = ""
            self.query_one("#issue-description").clear()
            self.query_one("#project-key-2").clear()
            self.query_one("#button-7").disabled = False
            self.call_from_thread(
                self.query_one("#product-team").remove_class, "visible"
            )
            self.call_from_thread(
                self.query_one("#product-team-label").remove_class, "visible"
            )
            self.call_from_thread(self.query_one("#summary").remove_class, "visible")
            self.call_from_thread(
                self.query_one("#summary-label").remove_class, "visible"
            )
            self.call_from_thread(self.query_one("#issue-type").remove_class, "visible")
            self.call_from_thread(
                self.query_one("#issue-type-label").remove_class, "visible"
            )
            self.call_from_thread(self.query_one("#bug-type").remove_class, "visible")
            self.call_from_thread(
                self.query_one("#bug-type-label").remove_class, "visible"
            )
            self.call_from_thread(
                self.query_one("#issue-description").remove_class, "visible"
            )
            self.call_from_thread(
                self.query_one("#issue-description-label").remove_class, "visible"
            )
            self.call_from_thread(self.query_one("#components").remove_class, "visible")
            self.call_from_thread(
                self.query_one("#components-label").remove_class, "visible"
            )
            self.call_from_thread(
                self.query_one("#affects-versions").remove_class, "visible"
            )
            self.call_from_thread(
                self.query_one("#affects-versions-label").remove_class, "visible"
            )
        except JIRAError:
            print(f"\033[1;31mPlease sync Jira project components\033[0m")
        finally:
            self.query_one("#button-7").disabled = False

    @work(exclusive=True, thread=True)
    def conversion(self) -> None:
        baseSHA = self.query_one("#base").value
        headSHA = self.query_one("#head").value
        repo_name = self.query_one("#repo-name").value

        self.query_one("#button-8").disabled = True

        self.query_one(RichLog).clear()
        self.query_one(RichLog).begin_capture_print()

        try:
            convert_commits_to_tickets.main(baseSHA, headSHA, repo_name)

            self.query_one("#base").value = ""
            self.query_one("#head").value = ""
            self.query_one("#repo-name").value = "liferay/liferay-portal"

        except (AssertionError, JIRAError):
            print(
                f"\033[1;31mPlease check your credentials in credentials-ext.properties\033[0m"
            )
        except TypeError:
            print(
                f"\033[1;31mPlease check if the {baseSHA} and\033[0m{os.linesep}\033[1;31mthe {headSHA} are in the same repository!\033[0m"
            )
        finally:
            self.query_one("#button-8").disabled = False

    @work(exclusive=True, thread=True)
    def forward_failure_pull_request(self) -> None:
        failure_pull_request_number = self.query_one(
            "#failure-pull-request-number"
        ).value

        self.query_one("#button-1").disabled = True

        self.query_one(RichLog).clear()
        self.query_one(RichLog).begin_capture_print()

        try:
            forward_failure_pull_request.main(failure_pull_request_number)

            self.query_one("#failure-pull-request-number").value = ""

        except (AssertionError, GitCommandError):
            print(
                f"\033[1;31mPlease check your credentials in credentials-ext.properties\033[0m"
            )
        finally:
            self.query_one("#button-1").disabled = False

    @work(exclusive=True, thread=True)
    def trigger_gauntlet(self) -> None:
        legacy_local_path = self.query_one("#legacy-repo-path").value
        target_branch = self.query_one("#target-branch").value

        self.query_one("#button-6").disabled = True

        self.query_one(RichLog).clear()
        self.query_one(RichLog).begin_capture_print()

        try:
            trigger_gauntlet.main(legacy_local_path, target_branch)

            self.query_one("#button-6").disabled = False
            self.query_one("#legacy-repo-path").value = credentials.get_credentials(
                "LEGACY_REPO_PATH"
            )
            self.query_one("#target-branch").value = "7.3.x"
        except (AssertionError, JIRAError, GitCommandError):
            print(
                f"\033[1;31mPlease check your credentials in credentials-ext.properties\033[0m"
            )
        finally:
            self.query_one("#button-6").disabled = False

    @work(exclusive=True, thread=True)
    def write_comments(self) -> None:
        ticket_number = self.query_one("#jira-ticket-number-4").value
        comments = self.query_one("#comments").text

        self.query_one("#button-4").disabled = True

        self.query_one(RichLog).clear()
        self.query_one(RichLog).begin_capture_print()

        try:
            write_comments.main(comments, ticket_number)

            self.query_one("#button-4").disabled = False
            self.query_one("#jira-ticket-number-4").value = ""
            self.query_one("#comments-type").clear()
            self.call_from_thread(self.query_one("#comments").remove_class, "visible")
            self.call_from_thread(
                self.query_one("#comments-label").remove_class, "visible"
            )
        except (AssertionError, JIRAError):
            print(
                f"\033[1;31mPlease check your credentials in credentials-ext.properties\033[0m"
            )
        finally:
            self.query_one("#button-4").disabled = False

    @work(exclusive=True, thread=True)
    def write_description(self) -> None:
        ticket_number = self.query_one("#jira-ticket-number-5").value
        description = self.query_one("#description").text

        self.query_one("#button-5").disabled = True

        self.query_one(RichLog).clear()
        self.query_one(RichLog).begin_capture_print()

        try:
            write_description.main(description, ticket_number)

            self.query_one("#button-5").disabled = False
            self.query_one("#jira-ticket-number-5").value = ""
            self.query_one("#description-type").clear()
            self.call_from_thread(
                self.query_one("#description").remove_class, "visible"
            )
            self.call_from_thread(
                self.query_one("#description-label").remove_class, "visible"
            )
        except (AssertionError, JIRAError):
            print(
                f"\033[1;31mPlease check your credentials in credentials-ext.properties\033[0m"
            )
        finally:
            self.query_one("#button-5").disabled = False

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
        elif event.button.id == "button-6":
            self.trigger_gauntlet()
        elif event.button.id == "button-7":
            self.create_issue()
        elif event.button.id == "button-8":
            self.conversion()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        self.query_one(ContentSwitcher).current = event.item.id

    def on_markdown_link_clicked(self, event: Markdown.LinkClicked) -> None:
        webbrowser.open(event.href)

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "description-type":
            try:
                description = generate_description(
                    self.query_one("#description-type").value
                )

                self.query_one("#description").load_text(description)
            except:
                pass

            self.query_one("#description").set_class(
                event.value != Select.BLANK, "visible"
            )
            self.query_one("#description-label").set_class(
                event.value != Select.BLANK, "visible"
            )

        elif event.select.id == "comments-type":
            try:
                comment = generate_comment(self.query_one("#comments-type").value)

                self.query_one("#comments").load_text(comment)
            except:
                pass

            self.query_one("#comments").set_class(
                event.value != Select.BLANK, "visible"
            )
            self.query_one("#comments-label").set_class(
                event.value != Select.BLANK, "visible"
            )

        elif event.select.id == "issue-type":
            try:
                comment = generate_comment(self.query_one("#issue-type").value)

                self.query_one("#comments").load_text(comment)
            except:
                pass

            self.query_one("#summary-label").set_class(
                event.value != Select.BLANK, "visible"
            )
            self.query_one("#summary").set_class(event.value != Select.BLANK, "visible")
            self.query_one("#issue-description-label").set_class(
                event.value != Select.BLANK, "visible"
            )
            self.query_one("#issue-description").set_class(
                event.value != Select.BLANK, "visible"
            )
            self.query_one("#bug-type").set_class(event.value == "Bug", "visible")
            self.query_one("#bug-type-label").set_class(event.value == "Bug", "visible")
            self.query_one("#components-label").set_class(
                event.value != Select.BLANK, "visible"
            )
            self.query_one("#components").set_class(
                event.value != Select.BLANK, "visible"
            )
            # self.query_one("#product-team").set_class(
            #     event.value == "Testing", "visible"
            # )
            # self.query_one("#product-team-label").set_class(
            #     event.value == "Testing", "visible"
            # )
            self.query_one("#affects-versions").set_class(
                event.value == "Bug", "visible"
            )
            self.query_one("#affects-versions-label").set_class(
                event.value == "Bug", "visible"
            )

        elif event.select.id == "bug-type":
            try:
                description = generate_description(self.query_one("#bug-type").value)

                self.query_one("#issue-description").load_text(description)
            except:
                pass

            self.query_one("#summary").set_class(event.value != Select.BLANK, "visible")
            self.query_one("#summary-label").set_class(
                event.value != Select.BLANK, "visible"
            )
            self.query_one("#components-label").set_class(
                event.value != Select.BLANK, "visible"
            )
            self.query_one("#components").set_class(
                event.value != Select.BLANK, "visible"
            )
            self.query_one("#issue-description-label").set_class(
                event.value != Select.BLANK, "visible"
            )
            self.query_one("#issue-description").set_class(
                event.value != Select.BLANK, "visible"
            )
        elif event.select.id == "product-team":
            if self.query_one("#product-team").value == Select.BLANK:
                self.query_one("#summary").value = ""
                self.query_one("#issue-description").clear()
            else:
                self.query_one("#summary").value = get_properties(
                    self.query_one("#product-team").value, "SUMMARY"
                )
                self.query_one("#issue-description").load_text(
                    get_properties(self.query_one("#product-team").value, "DESCRIPTION")
                )
        elif event.select.id == "project-key-2":
            if self.query_one("#project-key-2").value != Select.BLANK:
                components = get_components(
                    f'{self.query_one("#project-key-2").value}_COMPONENTS'
                )

                self.query_one("#components").set_options((eval(components)))

            else:
                self.query_one("#product-team").clear()
                self.query_one("#summary").value = ""
                self.query_one("#components").clear()
                self.query_one("#issue-type").clear()
                self.query_one("#issue-description").clear()
                self.query_one("#assign-to-me-2").value = False
                self.query_one("#issue-label").value = ""
                self.query_one("#components").remove_class("visible")
                self.query_one("#components-label").remove_class("visible")
                self.query_one("#product-team").remove_class("visible")
                self.query_one("#product-team-label").remove_class("visible")
                self.query_one("#affects-versions").remove_class("visible")
                self.query_one("#affects-versions-label").remove_class("visible")
                self.query_one("#bug-type").remove_class("visible")
                self.query_one("#bug-type-label").remove_class("visible")
                self.query_one("#summary").remove_class("visible")
                self.query_one("#summary-label").remove_class("visible")
                self.query_one("#issue-description").remove_class("visible")
                self.query_one("#issue-description-label").remove_class("visible")


app = ScriptApp()

if __name__ == "__main__":
    app.run()
