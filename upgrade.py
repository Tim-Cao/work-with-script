import subprocess
import sys

subprocess.check_call(
    [sys.executable, "-m", "pip", "install", "--upgrade", "jproperties"]
)

subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pandas"])

subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "jira"])

subprocess.check_call(
    [sys.executable, "-m", "pip", "install", "--upgrade", "jsonpath-ng"]
)

subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "PyGithub"])

subprocess.check_call(
    [sys.executable, "-m", "pip", "install", "--upgrade", "GitPython"]
)

subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "textual"])
