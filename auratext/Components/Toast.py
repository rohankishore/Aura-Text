import os
import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect, QApplication
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QPoint, QEasingCurve
from PyQt6.QtGui import QColor, QFont, QIcon
from auratext.Misc.boilerplates import get_appdata_dirs

class ToastWidget(QWidget):
    def __init__(self, message, toast_type="info", parent=None, manager=None):
        super().__init__(parent)
        self.message = message
        self.toast_type = toast_type.lower()
        self.manager = manager
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.SubWindow)
        
        # Colors based on type
        colors = {
            "success": ("#22c55e", "Success"),
            "warning": ("#eab308", "Warning"),
            "error": ("#ef4444", "Error"),
            "info": ("#3b82f6", "Info")
        }
        accent_color, title_text = colors.get(self.toast_type, ("#3b82f6", "Info"))
        
        # Determine theme and glass config
        active_window = parent or QApplication.activeWindow()
        config = getattr(active_window, "_config", {})
        is_glass = config.get("cmdpaletteglass", "true").lower() == "true"
        theme_bg = "#1e1d23"
        if active_window and hasattr(active_window, "_themes"):
            theme_bg = active_window._themes.get("editor_theme", "#1e1d23")
            
        bg_color = "rgba(30, 30, 35, 0.92)" if is_glass else theme_bg
        border_color = "rgba(255, 255, 255, 0.15)" if is_glass else "rgba(255, 255, 255, 0.08)"

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Container Widget for Shadow
        self.container = QWidget(self)
        self.container.setObjectName("Container")
        self.container.setStyleSheet(f"""
            QWidget#Container {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 8px;
            }}
        """)
        layout.addWidget(self.container)
        
        # Add Drop Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setColor(QColor(0, 0, 0, 130))
        shadow.setOffset(0, 3)
        self.container.setGraphicsEffect(shadow)
        
        # Content Layout
        content_layout = QHBoxLayout(self.container)
        content_layout.setContentsMargins(12, 10, 12, 10)
        content_layout.setSpacing(10)
        
        # Left Accent Line
        self.accent_line = QWidget(self.container)
        self.accent_line.setFixedWidth(4)
        self.accent_line.setStyleSheet(f"background-color: {accent_color}; border-radius: 2px;")
        content_layout.addWidget(self.accent_line)
        
        # Message Section
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        self.title_label = QLabel(title_text)
        self.title_label.setStyleSheet(f"color: {accent_color}; font-size: 11px; font-weight: bold; background: transparent;")
        text_layout.addWidget(self.title_label)
        
        self.msg_label = QLabel(message)
        self.msg_label.setStyleSheet("color: #e1e1e6; font-size: 13px; background: transparent;")
        self.msg_label.setWordWrap(True)
        text_layout.addWidget(self.msg_label)
        
        content_layout.addLayout(text_layout)
        
        # Close Button
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(18, 18)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #a5a5b2;
                border: none;
                font-size: 16px;
                font-weight: bold;
                padding: 0;
            }
            QPushButton:hover {
                color: #ffffff;
            }
        """)
        self.close_btn.clicked.connect(self.fade_out)
        content_layout.addWidget(self.close_btn)
        
        self.setFixedSize(320, 75)
        
        # Timer to auto dismiss
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.fade_out)
        self.timer.start(4000) # 4 seconds

    def fade_out(self):
        self.timer.stop()
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QEasingCurve.Type.InBack)
        # Slide off screen to the right
        end_pos = QPoint(self.parent().width(), self.y())
        self.anim.setStartValue(self.pos())
        self.anim.setEndValue(end_pos)
        self.anim.finished.connect(self.close_and_remove)
        self.anim.start()

    def close_and_remove(self):
        self.close()
        if self.manager:
            self.manager.remove_toast(self)


class ToastManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.active_toasts = []
        self.history = []
        self.on_history_changed = None

    def show_toast(self, message, toast_type="info"):
        # Log to history
        self.history.append({"message": message, "type": toast_type, "time": QTimer.singleShot})
        if self.on_history_changed:
            self.on_history_changed()

        toast = ToastWidget(message, toast_type, self.main_window, self)
        self.active_toasts.append(toast)
        
        # Position the new toast
        self.reposition_toasts()
        toast.show()
        
        # Slide-in animation
        # Start from off-screen on the right
        start_x = self.main_window.width()
        start_y = toast.y()
        toast.move(start_x, start_y)
        
        toast.anim = QPropertyAnimation(toast, b"pos")
        toast.anim.setDuration(300)
        toast.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        toast.anim.setStartValue(QPoint(start_x, start_y))
        toast.anim.setEndValue(QPoint(self.main_window.width() - toast.width() - 20, start_y))
        toast.anim.start()

    def remove_toast(self, toast):
        if toast in self.active_toasts:
            self.active_toasts.remove(toast)
            self.reposition_toasts()

    def reposition_toasts(self):
        # Calculate stacking positions from bottom-right (above status bar if shown)
        status_bar_height = 0
        if hasattr(self.main_window, "statusBar") and self.main_window.statusBar.isVisible():
            status_bar_height = self.main_window.statusBar.height()
            
        base_y = self.main_window.height() - status_bar_height - 20
        x = self.main_window.width() - 320 - 20
        
        for i, toast in enumerate(reversed(self.active_toasts)):
            target_y = base_y - ((i + 1) * (toast.height() + 10))
            if toast.isVisible() and not getattr(toast, "anim", None):
                toast.move(x, target_y)
            elif toast.isVisible() and getattr(toast, "anim", None):
                # If animation is running, update the target end position
                toast.anim.setEndValue(QPoint(x, target_y))
            else:
                toast.move(x, target_y)
