import sqlite3

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QHBoxLayout)
from PyQt6.QtWidgets import QVBoxLayout, QDialog, QScrollArea
from qfluentwidgets import (CardWidget, IconWidget, BodyLabel, CaptionLabel)
from qfluentwidgets import (RoundMenu, Action, FluentIcon)
from qfluentwidgets import (CardWidget, IconWidget, BodyLabel, CaptionLabel, TransparentToolButton, FluentIcon,
                            RoundMenu, Action, ImageLabel, SimpleCardWidget,
                            HeaderCardWidget, HyperlinkLabel, PrimaryPushButton, TitleLabel, PillPushButton, setFont,
                            VerticalSeparator)

class AppointmentsCard(CardWidget):
    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        # self.openButton = PushButton('', self)
        # self.openButton.setIcon(FluentIcon.RIGHT_ARROW)
        self.moreButton = TransparentToolButton(FluentIcon.RIGHT_ARROW, self)

        self.parent = parent

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
        self.hBoxLayout.addWidget(self.moreButton, 0, Qt.AlignmentFlag.AlignRight)

        self.moreButton.setFixedSize(32, 32)
        self.moreButton.clicked.connect(self.onMoreButtonClicked)

    def onMoreButtonClicked(self):
        menu = RoundMenu(parent=self)
        view_todays_todo = Action(FluentIcon.VIEW, "Remove from Recent", self)
        view_todays_todo.triggered.connect(self.parent.remove_project_from_recent)
        menu.addAction(view_todays_todo)

        x = (self.moreButton.width() - menu.width()) // 2 + 10
        pos = self.moreButton.mapToGlobal(QPoint(x, self.moreButton.height()))
        menu.exec(pos)

        #def onMoreButtonClicked(self):
         #   self.parent.today_todo()


class ProjectManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Manage Projects")
        self.setMinimumWidth(600)

        self.localappdata = parent.local_app_data
        self._themes = parent._themes

        self.conn = sqlite3.connect(f"{self.localappdata}/data/ProjectManager.db")
        self.dbcursor = self.conn.cursor()


        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.scroll_area = QScrollArea()
        self.scroll_layout = QVBoxLayout(self.scroll_area)
        self.scroll_area.setLayout(self.scroll_layout)

        self.main_layout.addWidget(self.scroll_area)

        days_rem_till_bday = 5

        self.addCard_V(QIcon(f"{self.localappdata}/icons/explorer_filled.png"),
                       f"{days_rem_till_bday}", "days remaining till birthday")


    def addCard_V(self, icon=None, title=None, content=None):
        card = AppointmentsCard(icon, title, content, self)
        self.scroll_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignTop)

    def remove_project_from_recent(self):
        pass
