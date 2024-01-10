import os
import sys
from typing import Optional

from textual.app import ComposeResult
from textual.containers import *
from textual.widgets import *

root = os.path.join(os.path.dirname(__file__), "../")

sys.path.append(root)


class TextField(Vertical):
    CSS_PATH = root + "/liferay/src/css/main.css"

    def __init__(self, field_label: Optional[str] = None, input_id: Optional[str] = None) -> None:
        super().__init__()
        self.field_label = field_label
        self.input_id = input_id

    def compose(self) -> ComposeResult:
        yield Label(self.field_label)
        yield Input(id=self.input_id)
