
from typing import Callable, Literal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QApplication, QGridLayout,
    QLineEdit, QPushButton, QScrollArea,
    QTableWidget, QLabel, QFrame,
    QAbstractItemView, QHeaderView, QMenu, QSizePolicy,
    QProgressBar, QCheckBox, QMainWindow,
    QStackedWidget, QMessageBox, QFileDialog, QToolBar,
    QLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

DAYS_OF_THE_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
MONTHS_OF_THE_YEAR = {
    "January": 31,
    "February": 29,
    "March": 31,
    "April": 30,
    "May": 31,
    "June": 30,
    "July": 31,
    "August": 31,
    "September": 30,
    "October": 31,
    "November": 30,
    "December": 31,
}


def get_attendance_time_interval(min_timeline_dates, max_timeline_dates):
    interval = None
    start_days = None
    end_days = None
    for index, (month, _) in enumerate(MONTHS_OF_THE_YEAR.items()):
        if min_timeline_dates.month == month:
            start_days = sum(list(MONTHS_OF_THE_YEAR.values())[:index]) + min_timeline_dates.date
        if max_timeline_dates.month == month:
            year_addition = (max_timeline_dates.year - min_timeline_dates.year) * 360
            end_days = sum(list(MONTHS_OF_THE_YEAR.values())[:index]) + max_timeline_dates.date + year_addition
        
        if start_days is not None and end_days is not None:
            diff = end_days - start_days
            week_amt = int(diff / 7)
            interval = week_amt, week_amt % 7
            break
    
    return interval


def create_widget(parent_layout: QLayout | None, layout_type: type[QHBoxLayout] | type[QVBoxLayout] | type[QGridLayout]):
    widget = QWidget()
    layout = layout_type()
    widget.setLayout(layout)
    
    if parent_layout is not None:
        parent_layout.addWidget(widget)
    
    return widget, layout

def create_scrollable_widget(parent_layout: QLayout | None, layout_type: type[QHBoxLayout] | type[QVBoxLayout]):
    scroll_widget = QScrollArea()
    scroll_widget.setWidgetResizable(True)
    
    widget = QWidget()
    scroll_widget.setWidget(widget)
    layout = layout_type(widget)
    
    if parent_layout is not None:
        parent_layout.addWidget(scroll_widget)
    
    return scroll_widget, layout



class TabViewWidget(QWidget):
    def __init__(self, bar_orientation: Literal["vertical", "horizontal"] = "horizontal"):
        super().__init__()
        self.bar_orientation = bar_orientation
        
        assert self.bar_orientation in ("vertical", "horizontal"), f"Invalid orientation: {self.bar_orientation}"
        
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        tab_layout_type = QHBoxLayout if self.bar_orientation == "horizontal" else QVBoxLayout
        main_layout_type = QHBoxLayout if self.bar_orientation == "vertical" else QVBoxLayout
        
        container = QWidget()
        layout = main_layout_type()
        container.setLayout(layout)
        
        self.tab_buttons: list[QPushButton] = []
        
        tab_widget = QWidget()
        tab_widget.setContentsMargins(0, 0, 0, 0)
        
        self.tab_layout = tab_layout_type()
        tab_widget.setLayout(self.tab_layout)
        
        self.stack = QStackedWidget()
        
        # for tab_name, widget in tab_widget_mapping.items():
        #     self.add(tab_name, widget)
            # tab_button = QPushButton(tab_name)
            # tab_button.setCheckable(True)
            # tab_button.clicked.connect(self._make_tab_clicked_func(index))
            # tab_button.setProperty("class", "HorizontalTab" if self.bar_orientation == "horizontal" else "VerticalTab")
            # tab_button.setContentsMargins(0, 0, 0, 0)
            
            # self.tab_layout.addWidget(tab_button)
            # self.stack.addWidget(widget)
            # widget.setContentsMargins(0, 0, 0, 0)
            
            # self.tab_buttons.append(tab_button)
        
        if self.bar_orientation == "vertical":
            self.tab_layout.addStretch()
        
        self.setContentsMargins(0, 0, 0, 0)
        tab_widget.setContentsMargins(0, 0, 0, 0)
        self.stack.setContentsMargins(0, 0, 0, 0)
        
        layout.addWidget(tab_widget)
        layout.addWidget(self.stack)
        
        self.tab_buttons[0].click()
        
        main_layout.addWidget(container)
    
    def _make_tab_clicked_func(self, index: int):
        def func():
            self.stack.setCurrentIndex(index)
            
            for i, button in enumerate(self.tab_buttons):
                if i != index:
                    button.setChecked(False)
        
        return func
    
    def add(self, tab_name: str, widget: QWidget):
        tab_button = QPushButton(tab_name)
        tab_button.setCheckable(True)
        tab_button.clicked.connect(self._make_tab_clicked_func(len(self.tab_buttons)))
        tab_button.setProperty("class", "HorizontalTab" if self.bar_orientation == "horizontal" else "VerticalTab")
        tab_button.setContentsMargins(0, 0, 0, 0)
        
        self.tab_layout.addWidget(tab_button)
        self.stack.addWidget(widget)
        widget.setContentsMargins(0, 0, 0, 0)
        
        self.tab_buttons.append(tab_button)



class OptionsMenu(QFrame):
    def __init__(self, options: dict[str, Callable], parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Popup)
        self.setFrameShape(QFrame.Shape.Box)
        # self.setStyleSheet("background-color: #f0f0f0; border: 1px solid #aaa;")
        
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
    def __init__(self, sonar_safety_limit: float):
        super().__init__()
        
        self.sonar_safety_limit = sonar_safety_limit
        
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        
        layout = QVBoxLayout(self)
        
        self.container = QWidget()
        self.main_layout = QVBoxLayout()
        self.container.setLayout(self.main_layout)
        
        layout.addWidget(self.container)
        
        self.sonar = SonarCanvas()
        
        self.main_layout.addWidget(self.sonar)
    
    def update_sonar(self, angles, distances):
        self.sonar.clear()
        self.sonar.draw_circle(self.sonar_safety_limit, c="red", s=5)
        self.sonar.update_sonar_data(angles, distances, c='green', s=10)

