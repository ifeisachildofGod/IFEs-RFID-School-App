
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QApplication,
    QLineEdit, QPushButton, QScrollArea,
    QTableWidget, QLabel, QFrame,
    QAbstractItemView, QHeaderView, QMenu, QSizePolicy,
    QProgressBar, QCheckBox, QMainWindow,
    QStackedWidget, QMessageBox, QFileDialog, QToolBar,
    QRadioButton
)
from PyQt6.QtCore import Qt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class LabeledField(QWidget):
    def __init__(self, title: str, inner_widget: QWidget, min_size: bool = True, parent=None):
        super().__init__(parent)
        
        self.setProperty("class", "LabeledField")
        
        if min_size:
            self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        
        self.setStyleSheet("""
            #labeled-title {
                color: grey;
                font-size: 11px;
                padding: 0 4px;
                padding-bottom: 0px;
            }
            #labeled-widget {
                border: 1px solid #aaa;
                border-radius: 6px;
            }
        """)
        
        # Title Label (floating effect)
        self.label = QLabel(title)
        self.label.setObjectName("labeled-title")
        self.label.setProperty("class", "labeled-title")
        
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Frame to wrap the actual widget with border
        self.widget = QWidget()
        self.widget.setObjectName("labeled-widget")
        self.widget.setProperty("class", "labeled-widget")
        
        widget_layout = QVBoxLayout(self.widget)
        # widget_layout.setContentsMargins(5, 0, 5, 5)  # leave space for label
        widget_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignLeft)
        widget_layout.addWidget(inner_widget)
        
        # Stack label over the widget
        main_layout = QVBoxLayout(self)
        # main_layout.setContentsMargins(4, 10, 4, 4)
        main_layout.setSpacing(0)
        # main_layout.addWidget(self.label)
        main_layout.addWidget(self.widget)
        
        self.setLayout(main_layout)

    def get_widget(self):
        return self.widget.findChild(QWidget)


class SonarCanvas(FigureCanvas):
    def __init__(self):
        fig = Figure(figsize=(6, 6), dpi=100)
        self.ax = fig.add_subplot(111, projection='polar')
        
        self.ylim = 40
        self.initialize(self.ylim)
        super().__init__(fig)
    
    def initialize(self, max_range: int):
        self.ylim = max(max_range, self.ylim)
        
        self.ax.set_ylim(0, self.ylim)  # Max range
        
        self.ax.set_theta_zero_location('N')
        self.ax.set_theta_direction(-1)
    
    def clear(self):
        self.ax.clear()
    
    def draw_circle(self, distance: int, **kwargs):
        self.initialize(distance)
        
        angles = np.linspace(0, 360, 180)
        angles_rad = np.deg2rad(angles)
        
        self.ax.scatter(angles_rad, [distance for _ in range(len(angles_rad))], **kwargs)
    
    def update_sonar_data(self, angles_deg, distances, **kwargs):
        self.initialize(max(max(distances), self.ax.get_ylim()[1]))
        
        angles_rad = np.deg2rad(angles_deg)
        self.ax.scatter(angles_rad, distances, **kwargs)
        self.draw()

class BarChartCanvas(FigureCanvas):
    def __init__(self, title: str, x_label: str, y_label: str):
        fig = Figure(figsize=(6, 5), dpi=100)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        
        self.axes.set_title(title)
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
    
    def bar(self, x_values, y_values, display_values = False, **kwargs):
        bars = self.axes.bar(x_values, y_values, **kwargs)
        
        # Optional: add value labels on top of each bar
        if display_values:
            for bar in bars:
                height = bar.get_height()
                self.axes.text(bar.get_x() + bar.get_width()/2, height + 0.5, f'{height}', 
                                      ha='center', va='bottom')
        
        self.draw()

class GraphCanvas(FigureCanvas):
    def __init__(self, title: str, x_label: str, y_label: str):
        fig = Figure(figsize=(5, 4), dpi=100)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.axes.set_title(title)
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
    
    def plot(self, x, y, **kwargs):
        self.axes.plot(x, y, **kwargs)
        self.axes.legend()
        self.draw()


