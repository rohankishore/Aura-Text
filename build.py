import subprocess
import sys
import os
import platform

def run_pyinstaller():
    try:
        main_script = 'main.py'

        cmd = [
            'pyinstaller',
            main_script,
            '--onedir',  # Create a single folder
            '-w',  # Makes it windowed
            '--name', '"Aura Text"',
            '--icon=icon.ico'
        ]

        # Run PyInstaller
        subprocess.check_call(cmd)

        print("Build successful.")
    except Exception as e:
        print(f"Build failed: {e}")

if __name__ == '__main__':
    run_pyinstaller()
