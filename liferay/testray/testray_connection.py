import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from liferay.util.credentials import get_credentials


def get_testray_connection():
    print("Testray authorizing...")

    return (get_credentials("TESTRAY_USER_NAME"), get_credentials("TESTRAY_PASSWORD"))