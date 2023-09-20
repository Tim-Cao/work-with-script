import os
import subprocess

from jproperties import Properties


def get_credentials(key):
    configs = Properties()

    with open(
        os.path.join(os.path.dirname(__file__), "../../")
        + "/credentials-ext.properties",
        "rb",
    ) as config_file:
        configs.load(config_file)

    return configs.get(key).data


def open_credentials():
    root = os.path.join(os.path.dirname(__file__), "../../")

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
    else:
        print("Opening credentials-ext.properties...")

    try:
        subprocess.check_call(["code", "-rg", "credentials-ext.properties"])
    except Exception as e:
        print(str(e))
