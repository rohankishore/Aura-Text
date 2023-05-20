from PyQt6.QtCore import QMimeData, QPoint, Qt
from PyQt6.QtGui import QCursor, QDrag, QPixmap, QRegion
from PyQt6.QtWidgets import QTabWidget

class TabWidget(QTabWidget):
    def __init__(self, parent=None, new=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.tabBar().setMouseTracking(True)
        self.setMovable(True)
        if new:
            TabWidget.setup(self)

    def __setstate__(self, data):
        self.__init__(new=False)
        self.setParent(data["parent"])
        for widget, tabname in data["tabs"]:
            self.addTab(widget, tabname)
        TabWidget.setup(self)

    def __getstate__(self):
        data = {
            "parent": self.parent(),
            "tabs": [],
        }
        tab_list = data["tabs"]
        for k in range(self.count()):
            tab_name = self.tabText(k)
            widget = self.widget(k)
            tab_list.append((widget, tab_name))
        return data

    def setup(self):
        pass

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.RightButton:
            return

        globalPos = self.mapToGlobal(e.pos())
        tabBar = self.tabBar()
        posInTab = tabBar.mapFromGlobal(globalPos)
        index = tabBar.tabAt(e.pos())
        tabBar.dragged_content = self.widget(index)
        tabBar.dragged_tabname = self.tabText(index)
        tabRect = tabBar.tabRect(index)

        pixmap = QPixmap(tabRect.size())
        tabBar.render(pixmap, QPoint(), QRegion(tabRect))
        mimeData = QMimeData()

        drag = QDrag(tabBar)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)

        cursor = QCursor(Qt.OpenHandCursor)

        drag.setHotSpot(e.pos() - posInTab)
        drag.setDragCursor(cursor.pixmap(), Qt.MoveAction)
        drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, e):
        e.accept()

    def dragLeaveEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        if e.source().parentWidget() == self:
            return

        e.setDropAction(Qt.MoveAction)
        e.accept()
        tabBar = e.source()
        self.addTab(tabBar.dragged_content, tabBar.dragged_tabname)