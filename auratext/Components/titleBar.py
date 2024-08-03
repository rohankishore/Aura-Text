from PyQt6.QtCore import QPoint, QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from ..scripts.color_scheme_loader import color_schemes
from ..scripts.def_path import resource
from .intMenuBar import menu_bar

titleIcon = resource(r"../media/icon.ico")
minimiseIcon = resource(r"../media/titlebar/minimise.svg")
maximiseIcon = resource(r"../media/titlebar/maximise.svg")
closeIcon = resource(r"../media/titlebar/close.svg")
workSpaceIcon = resource(r"../media/titlebar/workspace.svg")
codespaceIcon = resource(r"../media/titlebar/codespace.svg")


class CustomTitleBar(QWidget):
    def __init__(self, zenithInstance=None, parent=None):
        super().__init__(parent)
        self.zenithInstance = zenithInstance
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet(f"background-color: {color_schemes['titlebar_bg']};")

        self.iconLabel = QLabel(self)
        self.iconLabel.setPixmap(QIcon(titleIcon).pixmap(15, 15))
        self.iconLabel.setStyleSheet("padding-left: 5px;")
        self.layout.addWidget(self.iconLabel, 0, Qt.AlignmentFlag.AlignLeft)

        self.menuBar = menu_bar(self, self.zenithInstance)
        self.layout.addWidget(self.menuBar, 0)

        self.titleLabel = QLabel("Nyxtext Zenith", self)
        self.layout.addWidget(self.titleLabel, 1, Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setStyleSheet(
            f"""
            color: {color_schemes['titlebar_fg']};
            font-style: italic;
            font-size: 12px;
            """
        )

        button_style = f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: {color_schemes['titlebar_button_hover']};
            }}
        """

        self.newWorkspaceButton = QPushButton(self)
        self.newWorkspaceButton.setIcon(QIcon(workSpaceIcon))
        self.newWorkspaceButton.setIconSize(QSize(12, 12))
        self.newWorkspaceButton.clicked.connect(self.zenithInstance.addNewWorkspace)
        self.layout.addWidget(self.newWorkspaceButton)
        self.newWorkspaceButton.setStyleSheet(button_style)

        self.newCodespaceButton = QPushButton(self)
        self.newCodespaceButton.setIcon(QIcon(codespaceIcon))
        self.newCodespaceButton.setIconSize(QSize(12, 12))
        self.newCodespaceButton.clicked.connect(self.zenithInstance.addNewCodespace)
        self.layout.addWidget(self.newCodespaceButton)
        self.newCodespaceButton.setStyleSheet(button_style)

        self.minimizeButton = QPushButton(self)
        self.minimizeButton.setIcon(QIcon(minimiseIcon))
        self.minimizeButton.setIconSize(QSize(12, 12))
        self.minimizeButton.clicked.connect(self.minimizeWindow)
        self.layout.addWidget(self.minimizeButton)
        self.minimizeButton.setStyleSheet(button_style)

        self.maximizeButton = QPushButton(self)
        self.maximizeButton.setIcon(QIcon(maximiseIcon))
        self.maximizeButton.setIconSize(QSize(12, 12))
        self.maximizeButton.clicked.connect(self.toggleMaximize)
        self.layout.addWidget(self.maximizeButton)
        self.maximizeButton.setStyleSheet(button_style)

        self.closeButton = QPushButton(self)
        self.closeButton.setIcon(QIcon(closeIcon))
        self.closeButton.setIconSize(QSize(12, 12))
        self.closeButton.clicked.connect(parent.closeApplication)
        self.layout.addWidget(self.closeButton)
        self.closeButton.setStyleSheet(button_style)

        self.setLayout(self.layout)
        self.isDragging = False
        self.dragPosition = QPoint()

    def toggleMaximize(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
        else:
            self.parent().showMaximized()

    def mouseDoubleClickEvent(self, event):
        self.toggleMaximize()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.isDragging = True
            self.dragPosition = event.globalPosition().toPoint() - self.parent().pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.isDragging:
            self.parent().move(event.globalPosition().toPoint() - self.dragPosition)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.isDragging = False

    def updateTitle(self, folderName=None, fileName=None):
        if folderName and fileName:
            self.titleLabel.setText(f"{folderName} - {fileName} - Zenith")
        elif fileName:
            self.titleLabel.setText(f"{fileName} - Zenith")
        else:
            self.titleLabel.setText("Zenith")

    def setup_minimal_titlebar(self):
        self.menuBar = menu_bar(self, self.zenithInstance)
        self.layout.addWidget(self.menuBar)

    def closeApplication(self):
        self.parent().close()

    def menuBar(self, zenithInstance):
        return menu_bar(self, zenithInstance)

    def minimizeWindow(self):
        self.parent().showMinimized()
