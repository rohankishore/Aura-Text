import subprocess
import sys
import os
import platform
import shutil

def run_pyinstaller():
    try:
        main_script = 'main.py'

        cmd = [
            'pyinstaller',
            main_script,
            '-w',  # Makes it windowed
            '--name', "Aura Text",
            '--icon=icon.ico',
            '--exclude-module', 'PyQt5'
        ]

        # Run PyInstaller
        subprocess.check_call(cmd)

        # Copy resources
        print("Copying resources...")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        dist_dir = os.path.join(script_dir, 'dist', 'Aura Text')
        shutil.copytree(os.path.join(script_dir, 'LocalAppData'), os.path.join(dist_dir, 'LocalAppData'), dirs_exist_ok=True)

        print("Build successful.")
    except Exception as e:
        print(f"Build failed: {e}")

if __name__ == '__main__':
    run_pyinstaller()
