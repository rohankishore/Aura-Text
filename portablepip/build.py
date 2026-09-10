import subprocess
import platform
import os
import pip

hooks_exclude_list = [
    "--exclude-module", "IPython",
    "--exclude-module", "numpy",
    "--exclude-module", "matplotlib",
    "--exclude-module", "PIL",
    "--exclude-module", "PyQt6",
    "--exclude-module", "zmq",
    "--exclude-module", "jedi",
    "--exclude-module", "parso",
    "--exclude-module", "pygments",
    "--exclude-module", "nbformat",
    "--exclude-module", "jsonschema",
    "--exclude-module", "jsonschema_specifications",
    "--exclude-module", "lark",
    "--exclude-module", "jinja2",
    "--exclude-module", "wcwidth",
    "--exclude-module", "matplotlib.backends",
    "--exclude-module", "matplotlib.pyplot",
    "--exclude-module", "matplotlib.backend_bases",
    "--exclude-module", "PIL.Image",
    "--exclude-module", "PIL.ImageFilter",
    "--exclude-module", "PIL.SpiderImagePlugin",
]

def run_pyinstaller():
    global hooks_exclude_list
    try:
        name = "portablepip"
        if platform.python_version().startswith('3'):
             name += "3"
        file_path = os.path.join(os.path.dirname(__file__), 'main.py')
        if platform.system() == "Windows":
            pythonexe = os.path.join(os.path.dirname(__file__), 'venv', 'Scripts', 'python.exe')
        else:
            pythonexe = os.path.join(os.path.dirname(__file__), 'venv', 'bin', 'python3')
        if not os.path.exists(pythonexe):
            raise FileNotFoundError("A venv python executable was not found. Please ensure that the virtual environment is set up correctly.")
        pip_path = pip.__path__[0]
        if platform.system() == "Windows":
            sep = ";"
        else:
            sep = ":"
        cmd = [pythonexe, '-m', 'PyInstaller', '--onefile', file_path, '--name', name, '--hidden-import', 'pip', '--add-data', f"{pip_path}{sep}pip", "--clean", '--noconfirm']
        cmd.extend(hooks_exclude_list)
        subprocess.check_call(cmd)
    except Exception as e:
            print(f"Build failed: {e}")

def main():
    run_pyinstaller()

if __name__ == '__main__':
    main()
