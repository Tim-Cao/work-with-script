import os
import sys
from typing import Optional

from textual.app import ComposeResult
from textual.containers import *
from textual.widgets import *

root = os.path.join(os.path.dirname(__file__), "../")

sys.path.append(root)


class TextAreaField(Vertical):
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
        yield TextArea(id=self.input_id, classes=self.text_classes)
