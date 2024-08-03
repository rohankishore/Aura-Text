from PyQt6.QtCore import QMimeData, QPoint
from PyQt6.QtGui import QPixmap, QRegion, QAction
from PyQt6.QtWidgets import QTabWidget, QMenu


class TabWidget(QTabWidget):
    def __init__(self, parent=None, new=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.tabBar().setMouseTracking(True)
        self.setMovable(True)
        self.setDocumentMode(True)
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
        globalPos = self.mapToGlobal(e.pos())
        tabBar = self.tabBar()
        posInTab = tabBar.mapFromGlobal(globalPos)
        index = tabBar.tabAt(e.pos())
        tabRect = tabBar.tabRect(index)

        pixmap = QPixmap(tabRect.size())
        tabBar.render(pixmap, QPoint(), QRegion(tabRect))
        mimeData = QMimeData()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        close_alltabs = QAction("Close All Tabs", self)

        close_alltabs.triggered.connect(self.close_all_tabs)

        menu.addAction(close_alltabs)

        menu.exec(event.globalPos())

    def close_all_tabs(self):
        self.clear()
