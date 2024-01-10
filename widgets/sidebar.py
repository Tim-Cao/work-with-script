import os
import sys

from textual.app import ComposeResult
from textual.containers import *
from textual.widgets import *

root = os.path.join(os.path.dirname(__file__), "../")

sys.path.append(root)


DETAILS = """
- **CTRL + O**

Open the `credentials-ext.properties`

- **CTRL + S**

Sync the Jira project components

- **CTRL + U**

Delete text to the left of the cursor

- **SHIFT + INSERT**

Paste text from the clipboard

&nbsp;

[Go to Documentation](https://github.com/Tim-Cao/work-with-script#work-with-script)
"""


class Sidebar(Container):
    CSS_PATH = root + "/liferay/src/css/main.css"

    def compose(self) -> ComposeResult:
        yield SidebarTitle("Shortcuts Details")
        yield Container(Markdown(DETAILS))


class SidebarTitle(Static):
    pass
