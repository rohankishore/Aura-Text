import psutil
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import QTimer, Qt

class PerformanceWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Performance")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        self.layout.addStretch()

        # CPU Usage
        self.cpu_label = QLabel("CPU Usage")
        self.cpu_progress = QProgressBar()
        self.cpu_progress.setRange(0, 100)
        self.cpu_progress.setTextVisible(True)
        self.layout.addWidget(self.cpu_label)
        self.layout.addWidget(self.cpu_progress)

        # Memory Usage
        self.mem_label = QLabel("Memory Usage")
        self.mem_progress = QProgressBar()
        self.mem_progress.setRange(0, 100)
        self.mem_progress.setTextVisible(True)
        self.layout.addWidget(self.mem_label)
        self.layout.addWidget(self.mem_progress)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_performance)
        self.timer.start(1000)  # Update every second

        self.update_performance()

    def update_performance(self):
        # CPU
        cpu_percent = psutil.cpu_percent(interval=None)
        self.cpu_progress.setValue(int(cpu_percent))
        self.cpu_progress.setFormat(f"{cpu_percent}%")

        # Memory
        memory = psutil.virtual_memory()
        mem_percent = memory.percent
        self.mem_progress.setValue(int(mem_percent))
        self.mem_progress.setFormat(f"{mem_percent}%")
