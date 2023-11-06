import os
import subprocess
import sys

root = os.path.dirname(__file__)

sys.path.append(root)

from liferay.util import credentials


def install_modules():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "jproperties"])

    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])

    subprocess.check_call([sys.executable, "-m", "pip", "install", "jira"])

    subprocess.check_call([sys.executable, "-m", "pip", "install", "jsonpath-ng"])

    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyGithub"])

    subprocess.check_call([sys.executable, "-m", "pip", "install", "GitPython"])

    subprocess.check_call([sys.executable, "-m", "pip", "install", "textual"])


if __name__ == "__main__":
    install_modules()

    credentials.generate_credentials()
