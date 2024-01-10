import os
import sys
from typing import Optional

from textual.app import ComposeResult
from textual.widgets import *

root = os.path.join(os.path.dirname(__file__), "../")

sys.path.append(root)


class Menubar(ListView):
    CSS_PATH = root + "/liferay/src/css/main.css"

    pass


class MenuItem(ListItem):
    CSS_PATH = root + "/liferay/src/css/main.css"

    def __init__(self, name: Optional[str] = None, id: Optional[str] = None) -> None:
        super().__init__()
        self._name = name
        self._id = id

    def compose(self) -> ComposeResult:
        yield Text(self._name, id=self._id)


class Text(Static):
    CSS_PATH = root + "/liferay/src/css/main.css"

    pass
