from lupa import LuaError, LuaRuntime  # type: ignore
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QMessageBox

lua = LuaRuntime(unpack_returned_tuples=True)


def key_shortcuts(main_window):
    filepath = r"zenith\shortcuts.lua"

    try:
        with open(filepath, "r") as file:
            lua_code = file.read()
        shortcuts = lua.execute(lua_code)

        toggle_file_tree_shortcut = QShortcut(
            QKeySequence(shortcuts["toggle_file_tree"]), main_window
        )
        toggle_file_tree_shortcut.activated.connect(
            main_window.fileTree.toggleFileTreeVisibility
        )

        next_tab_shortcut = QShortcut(QKeySequence(shortcuts["next_tab"]), main_window)
        next_tab_shortcut.activated.connect(main_window.nextTab)

        prev_tab_shortcut = QShortcut(QKeySequence(shortcuts["prev_tab"]), main_window)
        prev_tab_shortcut.activated.connect(main_window.prevTab)

        toggle_edit_mode_shortcut = QShortcut(
            QKeySequence(shortcuts["edit_mode"]), main_window
        )
        toggle_edit_mode_shortcut.activated.connect(main_window.toggleEditMode)

        show_calltip_shortcut = QShortcut(
            QKeySequence(shortcuts["show_call_tips"]), main_window
        )
        show_calltip_shortcut.activated.connect(main_window.show_calltip)

        show_autocompletion_shortcut = QShortcut(
            QKeySequence(shortcuts["show_autocompletion"]), main_window
        )
        show_autocompletion_shortcut.activated.connect(main_window.show_autocompletion)

        zoom_in_shortcut = QShortcut(QKeySequence(shortcuts["zoom_in"]), main_window)
        zoom_in_shortcut.activated.connect(main_window.zoom_in_font)

        zoom_out_shortcut = QShortcut(QKeySequence(shortcuts["zoom_out"]), main_window)
        zoom_out_shortcut.activated.connect(main_window.zoom_out_font)

        toggle_terminal_shortcut = QShortcut(
            QKeySequence(shortcuts["toggle_terminal"]), main_window
        )
        toggle_terminal_shortcut.activated.connect(main_window.toggleTerminal)

        maximize_shortcut = QShortcut(QKeySequence(shortcuts["maximize"]), main_window)
        maximize_shortcut.activated.connect(main_window.titleBar.toggleMaximize)

        minimize_shortcut = QShortcut(QKeySequence(shortcuts["minimize"]), main_window)
        minimize_shortcut.activated.connect(main_window.showMinimized)

        close_shortcut = QShortcut(QKeySequence(shortcuts["close"]), main_window)
        close_shortcut.activated.connect(main_window.close)

    except LuaError as e:
        QMessageBox.warning(main_window, "Error", f"Error executing Lua script: {e}")
    except FileNotFoundError:
        QMessageBox.warning(
            main_window, "Error", f"Shortcuts file not found: {filepath}"
        )
    except Exception as e:
        QMessageBox.warning(main_window, "Error", f"An unexpected error occurred: {e}")
