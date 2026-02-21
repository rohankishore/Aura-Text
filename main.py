import json
import os
import shutil
import platform

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
print(local_app_data)

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
    main()
