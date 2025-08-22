import shutil
import os
import sys
import platform

print("Starting installation...")

print("Retrieving environment variables...")
if platform.system() == "Windows":
    localappdata = os.getenv('LOCALAPPDATA')
elif platform.system() == "Linux":
    localappdata = os.path.expanduser("~/.config")
elif platform.system() == "Darwin":
    localappdata = os.path.expanduser("~/Library/Application Support")
else:
    print("Unsupported operating system")
    sys.exit(1)
print(f"Local AppData is {localappdata}")
programs = os.path.join(localappdata, "Programs", "Aura-Text")
print(f"Installation directory is {programs}")

print("Copying files...")
print("LocalAppData/AuraText")
shutil.copytree("LocalAppData/AuraText", os.path.join(localappdata, "AuraText"), dirs_exist_ok=True)
print("Aura-Text")
shutil.copytree(os.getcwd(), programs, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git"))

if platform.system() != "Windows":
    print("Making executable...")
    os.system(f"chmod +x {os.path.join(programs, 'aura-text')}")

print("Installing dependencies...")
exit_code = os.system(f'"{sys.executable}" -m pip install -r requirements.txt')
if exit_code == 256:
    exit_code = os.system(f'"{sys.executable}" -m pip install -r requirements.txt --break-system-packages')
else:
    print(f"Installation failed with exit code {exit_code} while installing dependencies.")
    sys.exit(exit_code)
if platform.system() == "Windows":
    exit_code2 = os.system(f'"{sys.executable}" -m pip install wheels\pyqtdarktheme-2.1.0-py3-none-any.whl')
    if exit_code2 == 256:
        exit_code2 = os.system(f'"{sys.executable}" -m pip install wheels\pyqtdarktheme-2.1.0-py3-none-any.whl --break-system-packages')
    else:
        print(f"Installation failed with exit code {exit_code2} while installing pyqtdarktheme.")
        sys.exit(exit_code2)
else:
    exit_code2 = os.system(f'"{sys.executable}" -m pip install wheels/pyqtdarktheme-2.1.0-py3-none-any.whl')
    if exit_code2 == 256:
        exit_code2 = os.system(f'"{sys.executable}" -m pip install wheels/pyqtdarktheme-2.1.0-py3-none-any.whl --break-system-packages')
    else:
        print(f"Installation failed with exit code {exit_code2} while installing pyqtdarktheme.")
        sys.exit(exit_code2)

print("Creating shortcuts...")
if platform.system() == "Windows":
    import winshell
    print("Desktop")
    desktop = winshell.desktop()
    shortcut_path = winshell.shortcut(os.path.join(os.path.join(desktop, "Aura Text.lnk")))
    shortcut_path.path = os.path.join(programs, "auratext.bat")
    shortcut_path.working_directory = programs
    shortcut_path.description = "Aura Text is a versatile and powerful text editor powered by QScintilla that provides all the necessary tools for developers. It is build using PyQt6 and Python."
    shortcut_path.icon_location = (os.path.join(programs, "icon.ico"), 0)
    shortcut_path.write()
    print("Start Menu")
    desktop = winshell.start_menu()
    shortcut_path = winshell.shortcut(os.path.join(os.path.join(desktop, "Aura Text.lnk")))
    shortcut_path.path = os.path.join(programs, "auratext.bat")
    shortcut_path.working_directory = programs
    shortcut_path.description = "Aura Text is a versatile and powerful text editor powered by QScintilla that provides all the necessary tools for developers. It is build using PyQt6 and Python."
    shortcut_path.icon_location = (os.path.join(programs, "icon.ico"), 0)
    shortcut_path.write()
else:
    print("bin")
    os.system("rm -f ~/.local/bin/auratext")
    os.system("ln -s Programs/aura-text ~/.local/bin/auratext")

print("Installation complete.")