"""
SVG Icon Manager for dynamic color changes based on selection state
"""
import os
import re
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtCore import QByteArray, Qt

try:
    from PyQt6.QtSvg import QSvgRenderer
    SVG_AVAILABLE = True
except ImportError:
    SVG_AVAILABLE = False
    print("Warning: PyQt6.QtSvg not available. Install with: pip install PyQt6-QtSvg")


class SVGIconManager:
    @staticmethod
    def create_colored_icon(svg_path, color=None, size=(24, 24)):
        """
        Create a QIcon from SVG with optional color replacement
        
        Args:
            svg_path: Path to SVG file
            color: Color to apply (QColor or hex string). If None, uses original colors
            size: Icon size as tuple (width, height)
        
        Returns:
            QIcon with the specified color
        """
        if not SVG_AVAILABLE:
            # Fallback to regular icon loading
            return QIcon(svg_path)
        
        if not os.path.exists(svg_path):
            return QIcon()
        
        # Read SVG file
        with open(svg_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        # If color is specified, replace fill colors in SVG
        if color:
            if isinstance(color, str):
                color_str = color
            elif isinstance(color, QColor):
                color_str = color.name()
            else:
                color_str = "#000000"
            
            # Replace fill attributes
            svg_content = re.sub(r'fill="[^"]*"', f'fill="{color_str}"', svg_content)
            svg_content = re.sub(r'stroke="[^"]*"', f'stroke="{color_str}"', svg_content)
            # Also handle style attributes
            svg_content = re.sub(r'fill:[^;"}]*', f'fill:{color_str}', svg_content)
            svg_content = re.sub(r'stroke:[^;"}]*', f'stroke:{color_str}', svg_content)
        
        # Create QPixmap from modified SVG
        svg_bytes = QByteArray(svg_content.encode('utf-8'))
        renderer = QSvgRenderer(svg_bytes)
        
        pixmap = QPixmap(size[0], size[1])
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        return QIcon(pixmap)
    
    @staticmethod
    def create_stateful_icon(svg_path, unselected_color=None, selected_color="#FFFFFF", size=(24, 24)):
        """
        Create icons for both selected and unselected states
        
        Args:
            svg_path: Path to SVG file
            unselected_color: Color for unselected state (None = original)
            selected_color: Color for selected state
            size: Icon size
            
        Returns:
            Tuple of (unselected_icon, selected_icon)
        """
        unselected_icon = SVGIconManager.create_colored_icon(svg_path, unselected_color, size)
        selected_icon = SVGIconManager.create_colored_icon(svg_path, selected_color, size)
        
        return unselected_icon, selected_icon
