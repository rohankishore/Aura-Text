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

        def showBracketMatchMessage(self, line):
            # Show a temporary message for bracket match
            msg = f"Bracket match found on line: {line}"
            self.showMessage(msg)
            QTimer.singleShot(4000, self.clearMessage)
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

            # ...existing code...

            self.addPermanentWidget(rightWidget)
            # ...existing code...
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
