import json
import os
import shutil
import platform

# Suppress noisy Qt startup warnings.
existing_qt_logging_rules = os.environ.get("QT_LOGGING_RULES", "").strip()
required_qt_rules = [
    "qt.qpa.window=false",
    "qt.text.font.db=false",
    "qt.text.font=false",
]
if existing_qt_logging_rules:
    rule_set = {rule.strip() for rule in existing_qt_logging_rules.split(";") if rule.strip()}
    for rule in required_qt_rules:
        rule_set.add(rule)
    os.environ["QT_LOGGING_RULES"] = ";".join(sorted(rule_set))
else:
    os.environ["QT_LOGGING_RULES"] = ";".join(required_qt_rules)

from PyQt6.QtWidgets import QApplication
import sys

from qt_material import apply_stylesheet

"""
The app will automatically check system platform and set the local app data path accordingly. 
It will then load the config and theme files to apply the user's settings and theme preferences.
"""

if platform.system() == "Windows":
    local_app_data = os.getenv('LOCALAPPDATA')
elif platform.system() == "Linux":
    local_app_data = os.path.expanduser("~/.config")
elif platform.system() == "Darwin":
    local_app_data = os.path.expanduser("~/Library/Application Support")
else:
    print("Unsupported operating system")
    sys.exit(1)
local_app_data = os.path.join(local_app_data, "AuraText")

if not os.path.exists(local_app_data):
    template_app_data = os.path.join(os.path.dirname(sys.executable), "LocalAppData", "AuraText")
    shutil.copytree(template_app_data, local_app_data)

from auratext.Core.window import Window
# from auratext.Core import get_started

""" 
This file includes the code to run the app. It also scans if the app is being opened for the first time in order to show the
setup instructions.
"""

with open(f"{local_app_data}/data/config.json", "r") as config_file:
    _config = json.load(config_file)
with open(f"{local_app_data}/data/theme.json", "r") as config_file:
    _theme = json.load(config_file)

import random

def main():
    app = QApplication(sys.argv)
    if _theme["theming"] == "material":
        theme = _theme["material_type"] + ".xml"
        apply_stylesheet(app, theme=theme)
    ex = Window()
    sys.exit(app.exec())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Aura Text interrupted by user.")
