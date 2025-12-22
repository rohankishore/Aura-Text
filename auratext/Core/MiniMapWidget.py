from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QFont, QFontMetrics, QPen, QBrush
from PyQt6.QtCore import Qt, QRect, QRectF, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty

class MiniMapWidget(QWidget):
    def __init__(self, editor=None, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.setMinimumWidth(100)
        self.setMaximumWidth(150)
        self.setSizePolicy(self.sizePolicy().horizontalPolicy(), self.sizePolicy().verticalPolicy())
        
        # Visual settings
        self.bg_color = QColor("#1e1e1e")
        self.text_color = QColor("#d4d4d4")
        self.keyword_color = QColor("#569cd6")
        self.string_color = QColor("#ce9178")
        self.comment_color = QColor("#6a9955")
        self.viewport_color = QColor("#264f78")
        self.viewport_border_color = QColor("#007acc")
        
        # Animation for smooth scrolling
        self._scroll_offset = 0.0
        self.scroll_animation = QPropertyAnimation(self, b"scroll_offset")
        self.scroll_animation.setDuration(150)
        self.scroll_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Cache
        self.cached_lines = []
        self.line_height = 2
        self.char_width = 1
        
        if self.editor:
            self._connect_editor_signals()
            
        # Update timer for smooth rendering
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self.update)
        
        self.setMouseTracking(True)

    @pyqtProperty(float)
    def scroll_offset(self):
        return self._scroll_offset
    
    @scroll_offset.setter
    def scroll_offset(self, value):
        self._scroll_offset = value
        self.update()

    def _connect_editor_signals(self):
        """Connect to editor signals"""
        if self.editor:
            self.editor.textChanged.connect(self._on_text_changed)
            self.editor.verticalScrollBar().valueChanged.connect(self._on_scroll)
            self.editor.cursorPositionChanged.connect(self._schedule_update)

    def _disconnect_editor_signals(self):
        """Disconnect from editor signals"""
        if self.editor:
            try:
                self.editor.textChanged.disconnect(self._on_text_changed)
                self.editor.verticalScrollBar().disconnect(self._on_scroll)
                self.editor.cursorPositionChanged.disconnect(self._schedule_update)
            except:
                pass

    def set_editor(self, editor):
        """Set a new editor for the minimap"""
        self._disconnect_editor_signals()
        self.editor = editor
        if self.editor:
            self._connect_editor_signals()
            self._update_cache()
        self.update()

    def _schedule_update(self):
        """Schedule an update with debouncing"""
        if not self.update_timer.isActive():
            self.update_timer.start(50)

    def _on_text_changed(self):
        """Handle text changes"""
        self._update_cache()
        self._schedule_update()

    def _on_scroll(self, value):
        """Handle scroll with smooth animation"""
        if not self.editor:
            return
        
        # Calculate target offset
        first_line = self.editor.firstVisibleLine()
        target_offset = first_line * self.line_height
        
        # Animate to target
        if abs(target_offset - self._scroll_offset) > 0.5:
            self.scroll_animation.stop()
            self.scroll_animation.setStartValue(self._scroll_offset)
            self.scroll_animation.setEndValue(target_offset)
            self.scroll_animation.start()
        else:
            self._scroll_offset = target_offset
            self.update()

    def _update_cache(self):
        """Update cached line data for faster rendering"""
        if not self.editor:
            return
            
        text = self.editor.text()
        self.cached_lines = text.split('\n')

    def paintEvent(self, event):
        """Paint the minimap with syntax highlighting"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
        
        # Fill background
        painter.fillRect(self.rect(), self.bg_color)
        
        if not self.editor or not self.cached_lines:
            painter.end()
            return
        
        # Setup minimap font
        font = QFont(self.editor.font().family())
        font.setPointSizeF(1.5)
        painter.setFont(font)
        
        # Calculate dimensions
        total_lines = len(self.cached_lines)
        available_height = self.height()
        self.line_height = max(2, available_height / max(total_lines, 1))
        
        # Draw code lines with basic syntax highlighting
        y_offset = 0
        for i, line in enumerate(self.cached_lines):
            if y_offset > self.height():
                break
                
            line_rect = QRectF(5, y_offset, self.width() - 10, self.line_height)
            
            # Draw line based on content
            if line.strip():
                color = self._get_line_color(line)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(color))
                
                # Draw as a thin bar representing code
                bar_width = min(len(line.strip()) * 0.5, self.width() - 15)
                painter.drawRect(QRectF(8, y_offset + 0.2, bar_width, self.line_height - 0.4))
            
            y_offset += self.line_height
        
        # Draw visible viewport indicator
        self._draw_viewport(painter)
        
        painter.end()

    def _get_line_color(self, line):
        """Get color for a line based on basic syntax detection"""
        stripped = line.strip()
        
        # Comments
        if stripped.startswith('#'):
            return self.comment_color
        
        # Strings
        if stripped.startswith('"') or stripped.startswith("'"):
            return self.string_color
        
        # Keywords (basic detection)
        keywords = ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'import', 'from', 'return', 'try', 'except']
        first_word = stripped.split()[0] if stripped.split() else ""
        if first_word in keywords:
            return self.keyword_color
        
        # Default text color
        return self.text_color

    def _draw_viewport(self, painter):
        """Draw the visible viewport indicator"""
        if not self.editor:
            return
        
        try:
            first_visible = self.editor.firstVisibleLine()
            visible_lines = self.editor.linesOnScreen()
            total_lines = len(self.cached_lines)
            
            if total_lines == 0:
                return
            
            # Calculate viewport rectangle
            viewport_top = (first_visible / total_lines) * self.height()
            viewport_height = (visible_lines / total_lines) * self.height()
            
            # Draw semi-transparent viewport background
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(self.viewport_color.red(), 
                                          self.viewport_color.green(), 
                                          self.viewport_color.blue(), 60)))
            painter.drawRect(QRectF(0, viewport_top, self.width(), viewport_height))
            
            # Draw viewport border
            painter.setPen(QPen(self.viewport_border_color, 1.5))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(QRectF(1, viewport_top, self.width() - 2, viewport_height))
            
        except Exception as e:
            pass  # Silently handle any edge cases

    def mousePressEvent(self, event):
        """Handle click to navigate"""
        if not self.editor or not self.cached_lines:
            return
        
        y_pos = event.position().y()
        total_lines = len(self.cached_lines)
        
        # Calculate which line was clicked
        clicked_ratio = y_pos / self.height()
        target_line = int(clicked_ratio * total_lines)
        
        # Scroll to that line
        if hasattr(self.editor, 'setFirstVisibleLine'):
            self.editor.setFirstVisibleLine(max(0, target_line))
        
        self.update()

    def wheelEvent(self, event):
        """Forward wheel events to editor"""
        if self.editor and self.editor.verticalScrollBar():
            delta = event.angleDelta().y()
            scrollbar = self.editor.verticalScrollBar()
            scrollbar.setValue(scrollbar.value() - delta // 4)
