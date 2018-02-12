"""
JSON Data Format
================

{
  "ports": {
    "4723": {
      "desired_caps": {
        "platformName": "Android",
        "platformVersion": "6.0.1",
        "device": "Google Nexus 5",
        "appPackageName": "com.android.settings",
        "appActivity": ".Settings",
        "noReset": "true",
        "fullReset": "false",
        "newCommandTimeout": 120,
        "udid": "0689fcced0b3613d"
      },
      "log_dir": "Log_123"
    }
}
"""

import json
from core.defaults import DESIRED_CAPS


def read_caps():
    with open(DESIRED_CAPS) as fh:
        data = json.load(fh)
        return data


def update_caps(caps):
    with open(DESIRED_CAPS, 'w') as fh:
        data = json.dump(caps, fh, indent=2)
        return data


def get_desired_caps(port):
    return read_caps()['ports'][port]['desired_caps']


def get_log_dir(port):
    return read_caps()['ports'][port]['log_dir']


def set_log_dir(port, dir_path):
    data = read_caps()
    data['ports'][port]['log_dir'] = dir_path
    return update_caps(data)
