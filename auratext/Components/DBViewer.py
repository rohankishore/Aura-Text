
import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableView, QTabWidget, QHeaderView
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel

class DBViewer(QWidget):
    def __init__(self, db_path):
        super().__init__()
        self.db_path = db_path
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.load_db()

    def load_db(self):
        con = sqlite3.connect(self.db_path)
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        con.close()

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(self.db_path)

        if not db.open():
            print(f"Error opening database: {db.lastError().text()}")
            return

        for table_name in tables:
            table_name = table_name[0]
            model = QSqlTableModel(db=db)
            model.setTable(table_name)
            model.select()

            view = QTableView()
            view.setModel(model)
            view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.tabs.addTab(view, table_name)
