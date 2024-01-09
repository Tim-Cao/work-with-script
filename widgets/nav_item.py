import os
import sys

from textual.widgets import *

root = os.path.join(os.path.dirname(__file__), "../")

sys.path.append(root)


class NavItem(Static):
    CSS_PATH = root + "/liferay/src/css/main.css"

    pass
