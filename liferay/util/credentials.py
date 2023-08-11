import os

from jproperties import Properties


def get_credentials(key):
    configs = Properties()

    with open(os.path.join(os.path.dirname(__file__), '../../') + '/credentials-ext.properties', 'rb') as config_file:
        configs.load(config_file)

    return configs.get(key).data