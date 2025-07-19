
from typing import Callable
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QScrollArea,
    QLabel, QFrame, QSizePolicy, QLayout
)

import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from matplotlib.figure import Figure
from models.data_models import CharacterName
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from others import *

class OptionsMenu(QFrame):
    def __init__(self, options: dict[str, Callable], parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Popup)
        self.setFrameShape(QFrame.Shape.Box)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        for option_name, option_func in options.items():
            btn = QPushButton(option_name)
            btn.clicked.connect(self.option_selected(option_func))
            layout.addWidget(btn)

    def option_selected(self, option_func: Callable):
        def func():
            option_func()
            self.hide()
        
        return func

class Image(QLabel):
    def __init__(self, path: str, parent=None, width: int | None = None, height: int | None = None):
        super().__init__(parent)
        
        pixmap = QPixmap(path)
        
        if width is not None or height is not None:
            if height is not None and width is None:
                self.setFixedSize(int(height * pixmap.size().width() / pixmap.size().height()), height)
            elif width is not None and height is None:
                self.setFixedSize(width, int(width * pixmap.size().height() / pixmap.size().width()))
            else:
                self.setFixedSize(width, height)
        
        self.setScaledContents(True)  # Optional: scale image to fit self
        scaled_pixmap = pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.setPixmap(scaled_pixmap)

class LabeledField(QWidget):
    def __init__(self, title: str, inner_widget: QWidget, width_size_policy: QSizePolicy.Policy | None = None, height_size_policy: QSizePolicy.Policy | None = None, parent=None):
        super().__init__(parent)
        
        if (width_size_policy, height_size_policy).count(None) != 2:
            self.setSizePolicy(width_size_policy if width_size_policy is not None else QSizePolicy.Policy.Preferred,
                               height_size_policy if height_size_policy is not None else QSizePolicy.Policy.Preferred)
        
        # Title Label (floating effect)
        self.label = QLabel(title)
        self.label.setProperty("class", "labeled-title")
        
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Frame to wrap the actual widget with border
        self.widget = QWidget()
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

class CharacterNameWidget(QWidget):
    def __init__(self, name: CharacterName):
        super().__init__()
        self.name = name
        
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        widget_2_1 = QWidget()
        layout_2_1 = QVBoxLayout()
        widget_2_1.setLayout(layout_2_1)
        
        widget_2_1_1 = QWidget()
        layout_2_1_1 = QHBoxLayout()
        widget_2_1_1.setLayout(layout_2_1_1)
        layout_2_1.addWidget(widget_2_1_1)
        
        name_1 = LabeledField("Surname", QLabel(self.name.sur))
        name_2 = LabeledField("First name", QLabel(self.name.first))
        name_3 = LabeledField("Middle name", QLabel(self.name.middle))
        
        layout_2_1_1.addWidget(name_1)
        layout_2_1_1.addWidget(name_2)
        layout_2_1_1.addWidget(name_3)
        
        widget_2_1_2 = QWidget()
        layout_2_1_2 = QHBoxLayout()
        widget_2_1_2.setLayout(layout_2_1_2)
        layout_2_1.addWidget(widget_2_1_2)
        
        name_4 = LabeledField("Other name", QLabel(self.name.other if self.name.other is not None else "No other name"))
        name_5 = LabeledField("Abbreviation", QLabel(self.name.abrev))
        
        layout_2_1_2.addWidget(name_4)
        layout_2_1_2.addWidget(name_5, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.main_layout.addWidget(LabeledField("Names", widget_2_1, height_size_policy=QSizePolicy.Policy.Maximum))



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



class BarWidget(QWidget):
    def __init__(self, title: str, x_label: str, y_label: str):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        
        layout = QVBoxLayout(self)
        
        self.container = QWidget()
        self.main_layout = QVBoxLayout()
        self.container.setLayout(self.main_layout)
        
        layout.addWidget(self.container)
        
        main_keys_widget = QWidget()
        self.main_keys_layout = QHBoxLayout()
        main_keys_widget.setLayout(self.main_keys_layout)
        
        self.bar_canvas = BarChartCanvas(title, x_label, y_label)
        
        self.main_layout.addWidget(main_keys_widget)
        self.main_layout.addWidget(self.bar_canvas)
    
    def add_data(self, name: str, color, data: tuple[list, list]):
        keys_widget, keys_layout = create_widget(None, QHBoxLayout)
        
        keys_widget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        
        key_frame = QFrame()
        key_frame.setStyleSheet(f"""
            background-color: {color};
            border: 1px solid black;
        """)
        key_frame.setFixedSize(20, 20)
        
        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        keys_layout.addWidget(key_frame)
        keys_layout.addWidget(name_label, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.bar_canvas.bar(data[0], data[1], True, color=color, edgecolor="black")
        
        self.main_keys_layout.addWidget(keys_widget, alignment=Qt.AlignmentFlag.AlignLeft)

class GraphWidget(QWidget):
    def __init__(self, title: str, x_label: str, y_label: str):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        
        layout = QVBoxLayout(self)
        
        self.container = QWidget()
        self.main_layout = QVBoxLayout()
        self.container.setLayout(self.main_layout)
        
        layout.addWidget(self.container)
        
        self.graph = GraphCanvas(title, x_label, y_label)
        self.main_layout.addWidget(self.graph)
    
    def plot(self, x, y, **kwargs):
        self.graph.plot(x, y, **kwargs)

class SonarWidget(QWidget):
    def __init__(self, safety_limit: float):
        super().__init__()
        
        self.safety_limit = safety_limit
        
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        
        layout = QVBoxLayout(self)
        
        self.container = QWidget()
        self.main_layout = QVBoxLayout()
        self.container.setLayout(self.main_layout)
        
        layout.addWidget(self.container)
        
        self.sonar = SonarCanvas()
        self.draw_safety_limit()
        
        self.main_layout.addWidget(self.sonar)
        
        self.latest_angles = None
        self.latest_distances = None
    
    def draw_safety_limit(self):
        self.sonar.draw_circle(self.safety_limit, c="red", s=5)
    
    def update_sonar(self, angles, distances):
        self.latest_angles = angles
        self.latest_distances = distances
        
        self.sonar.clear()
        self.draw_safety_limit()
        if None not in (self.latest_angles, self.latest_distances):
            self.sonar.update_sonar_data(self.latest_angles, self.latest_distances, c='green', s=10)
        else:
            self.sonar.draw()



