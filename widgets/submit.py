import os
import sys
from typing import Optional

from textual.widgets import *

root = os.path.join(os.path.dirname(__file__), "../")

sys.path.append(root)


class Submit(Button):
    CSS_PATH = root + "/liferay/src/css/main.css"

    def __init__(self, id: Optional[str] = None, disabled: bool = False) -> None:
        super().__init__(
            label="Submit",
            variant="primary",
            id=id,
            disabled=disabled,
        )
