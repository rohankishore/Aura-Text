import subprocess
import platform
import os
import pip

def run_pyinstaller():
    try:
        name = "portablepip"
        if platform.python_version().startswith('3'):
             name += "3"
        file_path = os.path.join(os.path.dirname(__file__), 'main.py')
        pip_path = pip.__path__[0]
        if platform.system() == "Windows":
            sep = ";"
        else:
            sep = ":"
        cmd = ['pyinstaller', '--onefile', file_path, '--name', name, '--hidden-import', 'pip', '--add-data', f"{pip_path}{sep}pip"]
        subprocess.check_call(cmd)
    except Exception as e:
            print(f"Build failed: {e}")

def main():
    run_pyinstaller()

if __name__ == '__main__':
    main()
