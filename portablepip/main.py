import sys
from pip._internal.cli.main import main

if "--pythonversion" in sys.argv:
    python_system_version = sys.version
    print(f"Built with Python {python_system_version}")
    sys.exit(0)

if __name__ == '__main__':
    sys.argv[0] = sys.argv[0].removesuffix('.exe')
    sys.exit(main())
