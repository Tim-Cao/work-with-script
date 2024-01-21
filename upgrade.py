import subprocess
import sys

for package in [
    "jproperties",
    "pandas",
    "jira",
    "jsonpath-ng",
    "PyGithub",
    "pyperclip",
    "GitPython",
    "textual",
]:
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--upgrade", package]
    )
