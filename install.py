import shutil
import os
import sys

print("Starting installation...")

print("Retrieving environment variables...")
localappdata = os.getenv('LOCALAPPDATA')
print(f"Local AppData is {localappdata}")
programs = os.path.join(localappdata, "Programs", "Aura-Text")
print(f"Installation directory is {programs}")

print("Copying files...")
print("LocalAppData\AuraText")
shutil.copytree("LocalAppData\AuraText", os.path.join(localappdata, "AuraText"), dirs_exist_ok=True)
print("Aura-Text")
shutil.copytree(os.getcwd(), programs, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git"))

print("Installing dependencies...")
exit_code = os.system(f'"{sys.executable}" -m pip install -r requirements.txt')
if exit_code != 0:
    print(f"Installation failed with exit code {exit_code} while installing dependencies.")
    sys.exit(exit_code)

print("Creating shortcuts...")
import winshell
desktop = winshell.desktop()
shortcut_path = winshell.shortcut(os.path.join(os.path.join(desktop, "Aura Text.lnk")))
shortcut_path.path = os.path.join(programs, "auratext.bat")
shortcut_path.working_directory = programs
shortcut_path.description = "Aura Text is a versatile and powerful text editor powered by QScintilla that provides all the necessary tools for developers. It is build using PyQt6 and Python."
shortcut_path.icon_location = (os.path.join(programs, "icon.ico"), 0)
shortcut_path.write()

print("Installation complete.")