import os
import sys
from typing import Optional

from textual.app import ComposeResult
from textual.containers import *
from textual.widgets import *

root = os.path.join(os.path.dirname(__file__), "../")

sys.path.append(root)


class Submit(Vertical):
    CSS_PATH = root + "/liferay/src/css/main.css"

    def __init__(self, button_id: Optional[str] = None) -> None:
        super().__init__()
        self.button_id = button_id

    def compose(self) -> ComposeResult:
        yield Static()
        yield Button("Submit", variant="primary", id=self.button_id)
