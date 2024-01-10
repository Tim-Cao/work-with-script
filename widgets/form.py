import os
import sys
from typing import Optional

from textual.containers import *

root = os.path.join(os.path.dirname(__file__), "../")

sys.path.append(root)


class Form(VerticalScroll):
    CSS_PATH = root + "/liferay/src/css/main.css"

    def __init__(self, id: Optional[str] = None) -> None:
        super().__init__(id=id)
