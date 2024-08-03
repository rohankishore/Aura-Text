from lupa import LuaRuntime  # type: ignore
from PyQt6.QtWidgets import QMessageBox

lua = LuaRuntime(unpack_returned_tuples=True)


def load_color_schemes():
    color_schemes = r"zenith\color_schemes.lua"
    try:
        with open(color_schemes, "r") as file:
            lua_code = file.read()
        color_schemes = lua.execute(lua_code)
        if color_schemes is None:
            raise ValueError("Lua script did not return a table")
        return dict(color_schemes)
    except FileNotFoundError:
        QMessageBox.warning(None, "Error", "Color schemes file not found.")
    except ValueError as e:
        QMessageBox.warning(None, "Error", f"Invalid color schemes file: {e}")
    except Exception as e:
        QMessageBox.warning(None, "Error", f"An unexpected error occurred: {e}")
    return {}


color_schemes = load_color_schemes()
