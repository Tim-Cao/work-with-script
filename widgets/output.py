import os
import sys

from rich.text import Text
from textual import on
from textual.app import events
from textual.widgets import *

root = os.path.join(os.path.dirname(__file__), "../")

sys.path.append(root)


class Output(RichLog):
    CSS_PATH = root + "/liferay/src/css/main.css"

    def __init__(self) -> None:
        super().__init__(highlight=True, markup=True)

    @on(events.Print)
    def on_print(self, event: events.Print) -> None:
        if event.text.strip():
            if "\033[" in event.text:
                self.write(Text.from_ansi(event.text))
            else:
                self.write(event.text)
