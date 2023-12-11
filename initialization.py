import os
import subprocess
import sys

root = os.path.dirname(__file__)

sys.path.append(root)


def install_modules():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "jproperties"])

    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])

    subprocess.check_call([sys.executable, "-m", "pip", "install", "jira"])

    subprocess.check_call([sys.executable, "-m", "pip", "install", "jsonpath-ng"])

    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyGithub"])

    subprocess.check_call([sys.executable, "-m", "pip", "install", "GitPython"])

    subprocess.check_call([sys.executable, "-m", "pip", "install", "textual"])


def generate_credentials():
    if os.path.exists(os.path.join(root, "credentials-ext.properties")) == False:
        print("Creating credentials-ext.properties...")

        with open(
            os.path.join(root, "credentials.properties"), "r"
        ) as credentials, open(
            os.path.join(root, "credentials-ext.properties"), "w"
        ) as credentials_ext:
            credentials_content = credentials.readlines()

            for line in range(7, len(credentials_content)):
                credentials_ext.write(credentials_content[line])

        print("credentials-ext.properties is created")


def upgrade_modules():
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--upgrade", "jproperties"]
    )

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pandas"]
    )

    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "jira"])

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--upgrade", "jsonpath-ng"]
    )

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--upgrade", "PyGithub"]
    )

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--upgrade", "GitPython"]
    )

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--upgrade", "textual"]
    )


if __name__ == "__main__":
    install_modules()

    upgrade_modules()

    generate_credentials()
