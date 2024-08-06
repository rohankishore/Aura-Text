import sqlite3
import os
from qfluentwidgets import (CardWidget, IconWidget, BodyLabel, CaptionLabel, FluentIcon,
                            RoundMenu, Action)
import subprocess
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QFont, QActionGroup, QFileSystemModel, QPixmap, QIcon
from PyQt6.Qsci import QsciScintilla
from PyQt6.QtWidgets import (
    QMainWindow,
    QInputDialog,
    QDockWidget,
    QTextEdit,
    QTreeView,
    QFileDialog,
    QSplashScreen,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QStatusBar, QHBoxLayout)

from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QMessageBox, QLineEdit, QDialog, QLabel, QComboBox, QSpacerItem, QScrollArea
from qfluentwidgets import (ScrollArea, ListWidget, RoundMenu, Action, FluentIcon, TitleLabel)


class AppCard(CardWidget):
    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        # self.openButton = PushButton('打开', self)
        # self.moreButton = TransparentToolButton(FluentIcon.MORE, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(48, 48)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        # self.openButton.setFixedWidth(120)

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
        # self.hBoxLayout.addWidget(self.openButton, 0, Qt.AlignmentFlag.AlignRight)
        # self.hBoxLayout.addWidget(self.moreButton, 0, Qt.AlignmentFlag.AlignRight)

        # self.moreButton.setFixedSize(32, 32)
        # self.moreButton.clicked.connect(self.onMoreButtonClicked)

    def onMoreButtonClicked(self):
        menu = RoundMenu(parent=self)
        menu.addAction(Action(FluentIcon.SHARE, '共享', self))
        menu.addAction(Action(FluentIcon.CHAT, '写评论', self))
        menu.addAction(Action(FluentIcon.PIN, '固定到任务栏', self))

        # x = (self.moreButton.width() - menu.width()) // 2 + 10
        # pos = self.moreButton.mapToGlobal(QPoint(x, self.moreButton.height()))
        # menu.exec(pos)



class ProjectManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Manage Projects")
        self.setGeometry(500, 700, 0, 0)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.scroll_area = QScrollArea()
        self.scroll_layout = QVBoxLayout(self.scroll_area)
        self.scroll_area.setLayout(self.scroll_layout)

        self.main_layout.addWidget(self.scroll_area)


    def addCard_V(self, icon=None, title=None, content=None):
        card = AppCard(icon, title, content, self)
        self.scroll_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignTop)

c = ProjectManager()
c.exec()