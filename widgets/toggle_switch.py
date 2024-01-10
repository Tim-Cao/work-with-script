import os
import sys
from typing import Optional

from textual.app import ComposeResult
from textual.containers import *
from textual.widgets import *

root = os.path.join(os.path.dirname(__file__), "../")

sys.path.append(root)


class ToggleSwitch(Vertical):
    CSS_PATH = root + "/liferay/src/css/main.css"

    def __init__(self, toggle_switch_id: Optional[str] = None) -> None:
        super().__init__()
        self.toggle_switch_id = toggle_switch_id

    def compose(self) -> ComposeResult:
        yield Static()
        with Horizontal():
            yield Switch(False, id=self.toggle_switch_id)
            yield Static("Assign to me (Optional)", classes="assign-to-me")
