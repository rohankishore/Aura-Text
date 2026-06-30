import subprocess
import sys
import os
import platform
import shutil
import urllib.request
import zipfile

def run_pyinstaller():
    try:
        main_script = 'main.py'

        cmd = [
            'pyinstaller',
            main_script,
            '-w',  # Makes it windowed
            '--name', "Aura Text",
            '--icon=icon.ico',
            '--exclude-module', 'PyQt5',
            '--add-data', 'notepadequalequal:notepadequalequal',
            '--add-data', 'lib2to3:lib2to3',
            '--add-data', 'auratext:auratext'
        ]

        # Run PyInstaller
        subprocess.check_call(cmd)

        # Copy resources
        print("Copying resources...")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        dist_dir = os.path.join(script_dir, 'dist', 'Aura Text')
        shutil.copytree(os.path.join(script_dir, 'LocalAppData'), os.path.join(dist_dir, 'LocalAppData'), dirs_exist_ok=True)
        if platform.system() == "Darwin":
            shutil.copytree(os.path.join(script_dir, 'LocalAppData'), os.path.join(script_dir, 'dist', 'Aura Text.app', 'Contents', 'MacOS', 'LocalAppData'), dirs_exist_ok=True)

        print("Build successful.")
    except Exception as e:
        print(f"Build failed: {e}")

def detect_portablepy_url():
    system = platform.system()

    if system == "Windows":
        url = "https://github.com/bjia56/portable-python/releases/download/cpython-v3.13.9-build.0/python-full-3.13.9-windows-x86_64.zip"
    elif system == "Darwin":
        url = "https://github.com/bjia56/portable-python/releases/download/cpython-v3.13.9-build.0/python-full-3.13.9-darwin-universal2.zip"
    elif system == "Linux":
        url = "https://github.com/bjia56/portable-python/releases/download/cpython-v3.13.9-build.0/python-full-3.13.9-linux-x86_64.zip"

    return url


def download_python(url, dest_dir):
    zip_path = os.path.join(dest_dir, "portable-python.zip")

    print("Downloading portable Python...")
    urllib.request.urlretrieve(url, zip_path)

    print("Extracting (flattening top-level folder)...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        members = zip_ref.namelist()
        # Identify top-level folder in the archive
        top_level = members[0].split("/")[0].rstrip("/")
        for member in members:
            if not member or member.endswith("/"):
                continue
            # Remove top-level folder prefix
            relative_path = os.path.relpath(member, top_level)
            # Safety check (avoid escaping target dir)
            if relative_path.startswith(".."):
                continue
            target_path = os.path.join(dest_dir, relative_path)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with zip_ref.open(member) as source, open(target_path, "wb") as target:
                target.write(source.read())

    os.remove(zip_path)
    print("Portable Python ready at:", dest_dir)


def chmod_bin(portable_python_dir):
    bin_dir = os.path.join(portable_python_dir, "bin")

    if os.path.isdir(bin_dir):
        subprocess.check_call(["chmod", "-R", "+x", bin_dir])

def main():
    run_pyinstaller()

    url = detect_portablepy_url()
    script_dir = os.path.dirname(__file__)
    dist_dir = os.path.join(script_dir, "dist", "Aura Text")
    portable_python_dir = os.path.join(dist_dir, "portable-python")
    os.makedirs(portable_python_dir, exist_ok=True)
    download_python(url, portable_python_dir)
    if platform.system() != "Windows":
        chmod_bin(portable_python_dir)
    if platform.system() == "Darwin":
        print("Running on macOS, so copying portable Python to app bundle as well...", end='')
        shutil.copytree(portable_python_dir, os.path.join(script_dir, 'dist', 'Aura Text.app', 'Contents', 'MacOS', 'portable-python'), dirs_exist_ok=True)
        print("done")

if __name__ == '__main__':
    main()

	

	
