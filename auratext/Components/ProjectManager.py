import os
import sqlite3
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QDialog, QScrollArea, QMessageBox
from qfluentwidgets import (
    CardWidget, IconWidget, BodyLabel, CaptionLabel, TransparentToolButton, FluentIcon,
    RoundMenu, Action
)

class AppointmentsCard(CardWidget):
    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.moreButton = TransparentToolButton(FluentIcon.RIGHT_ARROW, self)

        self.parent = parent

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(48, 48)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.moreButton, 0, Qt.AlignmentFlag.AlignRight)

        self.moreButton.setFixedSize(32, 32)
        self.moreButton.clicked.connect(self.onMoreButtonClicked)

    def onMoreButtonClicked(self):
        menu = RoundMenu(parent=self)
        remove_action = Action(FluentIcon.VIEW, "Remove from Recent", self)
        remove_action.triggered.connect(self.onRemoveClicked)
        menu.addAction(remove_action)

        x = (self.moreButton.width() - menu.width()) // 2 + 10
        pos = self.moreButton.mapToGlobal(QPoint(x, self.moreButton.height()))
        menu.exec(pos)

    def onRemoveClicked(self):
        if self.parent:
            self.parent.remove_project_from_recent(self.titleLabel.text(), self.contentLabel.text())

class ProjectManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Manage Projects")
        self.setMinimumWidth(600)

        self.localappdata = parent.local_app_data
        self._themes = parent._themes

        self.conn = sqlite3.connect(f"{self.localappdata}/data/ProjectManager.db")
        self.dbcursor = self.conn.cursor()

        self.dbcursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                path TEXT
            )
        ''')

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.scroll_area = QScrollArea()
        self.scroll_layout = QVBoxLayout(self.scroll_area)
        self.scroll_area.setLayout(self.scroll_layout)

        self.main_layout.addWidget(self.scroll_area)

        self.load_todos()

    def addCard_V(self, icon=None, title=None, content=None):
        card = AppointmentsCard(icon, title, content, self)
        self.scroll_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignTop)

    def remove_project_from_recent(self, name, path):
        try:
            self.dbcursor.execute('DELETE FROM projects WHERE name = ? AND path = ?', (name, path))
            self.conn.commit()
            QMessageBox.information(self, "Success", f"Removed {name} from recent projects.")
            try:
                self.refresh_projects()
            except Exception as e:
                print(e)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to remove project: {str(e)}")

    def load_todos(self):
        self.dbcursor.execute('SELECT name, path FROM projects')
        todos = self.dbcursor.fetchall()
        try:
            for name, path in todos:
                self.addCard_V(QIcon(f"{self.localappdata}/icons/explorer_filled.png"), name, path)
        except:
            pass

    def refresh_projects(self):
        try:
            for i in reversed(range(self.scroll_layout.count())):
                widget = self.scroll_layout.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)

            self.load_todos()
        except:
            pass
