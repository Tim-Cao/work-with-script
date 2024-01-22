import os
import sys
from typing import Optional

from textual import work
from textual.app import ComposeResult, events
from textual.widgets import *
from textual.binding import Binding
import pyperclip
from textual.containers import *

root = os.path.join(os.path.dirname(__file__), "../")

sys.path.append(root)


class TextAreaField(TextArea):
    BINDINGS = [
        Binding("ctrl+c", "copy_to_clipboard", show=False),
        Binding("ctrl+v", "paste_from_clipboard", show=False),
        Binding("escape", "quit", "Quit"),
    ]

    @work(exclusive=True, thread=True)
    def action_copy_to_clipboard(self) -> None:
        text_to_copy = self.selected_text

        pyperclip.copy(text_to_copy)

    @work(exclusive=True, thread=True)
    def action_paste_from_clipboard(self) -> None:
        self.replace(
            pyperclip.paste(),
            self.selection.start,
            self.selection.end,
        )


class TextAreaGroup(Vertical):
    CSS_PATH = root + "/liferay/src/css/main.css"

    def __init__(
        self,
        field_label: Optional[str] = None,
        input_id: Optional[str] = None,
        text_classes: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.field_label = field_label
        self.field_id = input_id + "-label"
        self.input_id = input_id
        self.text_classes = text_classes

    def compose(self) -> ComposeResult:
        yield Label(self.field_label, id=self.field_id, classes=self.text_classes)
        yield TextAreaField(id=self.input_id, classes=self.text_classes)
