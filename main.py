import json
import os
import shutil
import platform
from auratext.Misc.quirks import copy_if_not_exists
from auratext.Misc.boilerplates import get_appdata_dirs

if platform.system() == "Linux":
    from auratext.Misc.quirks import get_linux_productname, crosvm_quirks
    if "crosvm" in get_linux_productname():
        crosvm_quirks()

# Suppress Qt startup warnings.
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

"""
The app will automatically check system platform and set the local app data path accordingly. 
It will then load the config and theme files to apply the user's settings and theme preferences.
"""

local_app_data, script_dir = get_appdata_dirs()

template_app_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "LocalAppData", "AuraText")
if not os.path.exists(template_app_data):
    template_app_data = os.path.join(os.path.dirname(sys.executable), "LocalAppData", "AuraText")
if not os.path.exists(local_app_data):
    print("Setting up appdata...")
    shutil.copytree(template_app_data, local_app_data)
else:
    print("Verifying appdata integrity...")
    shutil.copytree(template_app_data, local_app_data, dirs_exist_ok=True, copy_function=copy_if_not_exists)

from auratext.Core.window import Window

""" 
This file includes the code to run the app. It also scans if the app is being opened for the first time in order to show the
setup instructions.
"""

with open(f"{local_app_data}/data/config.json", "r") as config_file:
    _config = json.load(config_file)
with open(f"{local_app_data}/data/theme.json", "r") as config_file:
    _theme = json.load(config_file)

def pathArgsHandler(ex, args):
    dirs = []
    files = []
    for path in args:
        if os.path.exists(path):
            if os.path.isdir(path):
                dirs.append(path)
            else:
                files.append(path)
    if dirs:
        ex.open_project(path=dirs[0])
    for file in files:
        ex.open_file_from_path(file)

def main():
    app = QApplication(sys.argv)
    if _theme["theming"] == "material":
        from qt_material import apply_stylesheet
        theme = _theme["material_type"] + ".xml"
        apply_stylesheet(app, theme=theme)
    ex = Window()
    pathArgsHandler(ex, sys.argv[1:])
    sys.exit(app.exec())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Aura Text interrupted by user.")
