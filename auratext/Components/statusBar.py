import json
import os
import time
import platform
import sys

from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QStatusBar, QWidget, QPushButton

# from ..scripts.color_scheme_loader import color_schemes

if platform.system() == "Windows":
    local_app_data = os.getenv('LOCALAPPDATA')
elif platform.system() == "Linux":
    local_app_data = os.path.expanduser("~/.config")
elif platform.system() == "Darwin":
    local_app_data = os.path.expanduser("~/Library/Application Support")
else:
    print("Unsupported operating system")
    sys.exit(1)
local_app_data = os.path.join(local_app_data, "AuraText")
with open(f"{local_app_data}/data/theme.json", "r") as themes_file:
    _themes = json.load(themes_file)

class Separator(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.VLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)


class StatusBar(QStatusBar):
    def __init__(self, parent=None, greeting=None):
        super().__init__(parent)
        #self.current_editor = parent.current_editor
        self.current_widget = parent.tab_widget.currentWidget()
        self.setStyleSheet(
            f"""
            QStatusBar {{
                background-color: {_themes['sidebar_bg']};
                color: {"#FFFFFF"};
                padding-bottom: 2px;
                position: absolute;
                bottom: 0;
            }}
            QStatusBar::item {{
                border: none;
            }}
            QLabel {{
                padding: 0 2px;
            }}
            """
        )

        
        smallFont = QFont()
        smallFont.setPointSize(8)

        # Always initialize editModeLabel first
        self.editModeLabel = QLabel("ReadOnly")
        self.editModeLabel.setFont(smallFont)
        self.editModeLabel.setStyleSheet(
            f"""
            color: {{"#FFFFFF;"}};
            font-weight: bold;
            margin-bottom: 5px;
            """
        )

        if greeting:
            self.greetingLabel = QLabel(greeting)
            self.greetingLabel.setFont(smallFont)
            self.addWidget(self.greetingLabel)

        # Tab Length Dropdown
        config_path = os.path.join(local_app_data, "data", "config.json")
        with open(config_path, "r") as f:
            config = json.load(f)
        self.tab_length_dropdown_visible = config.get("tab_length_dropdown", "True") == "True"
        self.tab_length = config.get("tab_length", 4)

        from PyQt6.QtWidgets import QComboBox
        self.tabLengthDropdown = QComboBox()
        self.tabLengthDropdown.setFont(smallFont)
        self.tabLengthDropdown.addItems(["2", "4", "6", "8"])
        self.tabLengthDropdown.setCurrentText(str(self.tab_length))
        self.tabLengthDropdown.setStyleSheet(
            "QComboBox { background-color: #222; color: #fff; border: none; padding: 2px 8px; }"
        )
        self.tabLengthDropdown.setToolTip("Tab Length")
        self.tabLengthDropdown.currentTextChanged.connect(self.save_tab_length)

        if self.tab_length_dropdown_visible:
            self.tabLengthDropdown.show()
        else:
            self.tabLengthDropdown.hide()

        self.lineLabel = QLabel("▼ Line:")
        self.lineValueLabel = QLabel("0")
        self.columnLabel = QLabel("▲ Column:")
        self.columnValueLabel = QLabel("0")
        self.totalLinesLabel = QLabel("∑ Total Lines:")
        self.totalLinesValueLabel = QLabel("0")
        self.wordsLabel = QLabel("⌁ Words:")
        self.wordsValueLabel = QLabel("0")
        
        # Language button
        self.languageButton = QPushButton("Plain Text")
        self.languageButton.setFont(smallFont)
        self.languageButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.languageButton.setStyleSheet(
            f"""
            QPushButton {{
                background-color: transparent;
                color: #FFFFFF;
                border: none;
                padding: 2px 8px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {_themes.get('sidebar_bg', '#2b2b2b')};
                text-decoration: underline;
            }}
            """
        )


        for label in [
            self.lineLabel,
            self.columnLabel,
            self.totalLinesLabel,
            self.wordsLabel,
        ]:
            label.setFont(smallFont)
            #label.setStyleSheet(f"color: {};")

        for label in [
            self.lineValueLabel,
            self.columnValueLabel,
            self.totalLinesValueLabel,
            self.wordsValueLabel,
        ]:
            label.setFont(smallFont)
            #label.setStyleSheet(f"color: ""/;")

        rightWidget = QWidget()
        rightLayout = QHBoxLayout(rightWidget)
        rightLayout.setContentsMargins(0, 0, 0, 5)
        rightLayout.setSpacing(1)

        rightLayout.addWidget(Separator())
        rightLayout.addWidget(self.lineLabel)
        rightLayout.addWidget(self.lineValueLabel)
        rightLayout.addWidget(Separator())
        rightLayout.addWidget(self.columnLabel)
        rightLayout.addWidget(self.columnValueLabel)
        rightLayout.addWidget(Separator())
        rightLayout.addWidget(self.totalLinesLabel)
        rightLayout.addWidget(self.totalLinesValueLabel)
        rightLayout.addWidget(Separator())
        rightLayout.addWidget(self.wordsLabel)
        rightLayout.addWidget(self.wordsValueLabel)
        rightLayout.addWidget(Separator())
        rightLayout.addWidget(self.languageButton)
        rightLayout.addWidget(Separator())

        # Insert tab length dropdown before last separator
        rightLayout.insertWidget(rightLayout.count()-1, self.tabLengthDropdown)
        rightLayout.insertWidget(rightLayout.count()-1, Separator())

        self.addPermanentWidget(rightWidget)
    def save_tab_length(self, value):
        config_path = os.path.join(local_app_data, "data", "config.json")
        with open(config_path, "r") as f:
            config = json.load(f)
        config["tab_length"] = int(value)
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)
        self.tab_length = int(value)
        # Optionally emit signal or call parent to update editor tab length


        self.editModeLabel = QLabel("ReadOnly")
        self.editModeLabel.setFont(smallFont)
        self.editModeLabel.setStyleSheet(
            f"""
            color: {"#FFFFFF;"};
            font-weight: bold;
            margin-bottom: 5px;
            """
        )

        self.addWidget(self.editModeLabel)

    def updateStats(self, line, column, total_lines, words):
        self.lineValueLabel.setText(str(line))
        self.columnValueLabel.setText(str(column))
        self.totalLinesValueLabel.setText(str(total_lines))
        self.wordsValueLabel.setText(str(words))

    def updateEditMode(self, mode):
        self.editModeLabel.setText(mode)
        #if mode == "ReadOnly":
        #    self.current_widget.setReadOnly(True)
        #else:
        #    self.current_widget.setReadOnly(False)
    
    def updateLanguage(self, language):
        """Update the language button text"""
        self.languageButton.setText(language)
    
    def setLanguageClickHandler(self, handler):
        """Set the click handler for the language button"""
        self.languageButton.clicked.connect(handler)
