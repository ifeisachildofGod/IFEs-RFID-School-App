import random
import sys
from typing import Callable, Literal
from matplotlib.cbook import flatten
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QApplication,
    QLineEdit, QPushButton, QScrollArea,
    QTableWidget, QLabel, QFrame,
    QAbstractItemView, QHeaderView, QMenu, QSizePolicy,
    QProgressBar, QCheckBox, QMainWindow,
    QStackedWidget, QMessageBox, QFileDialog, QToolBar,
)
from app_sections import *
from models import *
from PyQt6.QtGui import QDrag, QDragEnterEvent, QDragMoveEvent, QDropEvent, QAction, QImage
from PyQt6.QtCore import Qt, QMimeData, QThread, QTimer

from theme import ThemeManager, THEME_MANAGER


addr = "00:19:08:36:3F:5C"
from PyQt6.QtWidgets import QWidget, QPushButton, QStackedLayout, QHBoxLayout, QVBoxLayout, QSizePolicy, QFrame
from PyQt6.QtCore import Qt


class TabViewWidget(QWidget):
    def __init__(self, tab_widget_mapping: dict[str, QWidget], bar_orientation: Literal["vertical", "horizontal"] = "horizontal"):
        super().__init__()
        assert bar_orientation in ("vertical", "horizontal"), f"Invalid orientation: {bar_orientation}"
        
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        tab_layout_type = QHBoxLayout if bar_orientation == "horizontal" else QVBoxLayout
        main_layout_type = QHBoxLayout if bar_orientation == "vertical" else QVBoxLayout
        
        container = QWidget()
        layout = main_layout_type()
        container.setLayout(layout)
        
        self.tab_buttons: list[QPushButton] = []
        
        tab_widget = QWidget()
        tab_widget.setContentsMargins(0, 0, 0, 0)
        
        tab_layout = tab_layout_type()
        tab_widget.setLayout(tab_layout)
        
        self.bar_orientation = bar_orientation
        
        self.stack = QStackedWidget()
        
        for index, (tab_name, widget) in enumerate(tab_widget_mapping.items()):
            tab_button = QPushButton(tab_name)
            tab_button.setCheckable(True)
            tab_button.clicked.connect(self._make_tab_clicked_func(index))
            tab_button.setProperty("class", "HorizontalTab" if bar_orientation == "horizontal" else "VerticalTab")
            tab_button.setContentsMargins(0, 0, 0, 0)
            
            tab_layout.addWidget(tab_button)
            self.stack.addWidget(widget)
            widget.setContentsMargins(0, 0, 0, 0)
            
            self.tab_buttons.append(tab_button)
        
        if bar_orientation == "vertical":
            tab_layout.addStretch()
        
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


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle(f"IFEs Attendance Tracker")
        
        self.setGeometry(100, 100, 1000, 700)
        
        self.create_menu_bar()
        self.create_tool_bar()
        
        # Create main container
        container = QWidget()
        main_layout = QHBoxLayout()
        
        container.setLayout(main_layout)
        
        # Create sidebar layout
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(0)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        
        gas_widget = SensorWidget(Sensor(SensorMeta("Gas", "Flying fish", "13.1.0.1", "Arduino inc"), "img.png"))
        flame_widget = SensorWidget(Sensor(SensorMeta("Fire", "Fire free", "10.0.0.1", "Arduino inc"), "img.png"))
        
        safety_widget, safety_layout = create_scrollable_widget(None, QVBoxLayout)
        
        safety_layout.addWidget(gas_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        safety_layout.addWidget(flame_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Create stacked widget for content
        main_layout.addWidget(TabViewWidget({
            "Staff": TabViewWidget(
                {
                    "Attendance": SchoolManager(),
                    "Attendance graph": SchoolManager(),
                    "Punctuality Graph": SchoolManager(),
                    "Editor": EditorWidget(),
                    },
                "vertical"),
            "Security": SchoolManager(),
            "Safety": safety_widget
            }))
        # main_layout.addWidget(TabViewWidget({"Attendance": TabViewWidget({"Attendance": SchoolManager(), "Security": SchoolManager(), "Safety": SchoolManager()}), "Security": SchoolManager(), "Safety": SchoolManager()}))
        
        self.setCentralWidget(container)
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("File") #type: ignore
        
        # Add File Actions
        new_action = QAction("New", self)
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        save_as_action = QAction("Save_as", self)
        exit_action = QAction("Exit", self)
        
        new_action.setShortcut("Ctrl+N")
        open_action.setShortcut("Ctrl+O")
        save_action.setShortcut("Ctrl+S")
        save_as_action.setShortcut("Ctrl+Shift+S")
        
        exit_action.triggered.connect(self.close)
        
        file_menu.addActions([new_action, open_action, save_action, save_as_action, exit_action]) #type: ignore
    
    def create_tool_bar(self):
        toolbar = QToolBar("Hello")
        self.toolBarArea(toolbar)
        
        a_action = QAction("Teachers", self)
        b_action = QAction("Prefects", self)
        c_action = QAction("Attendace", self)
        
        toolbar.addActions([a_action, b_action, c_action])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    THEME_MANAGER.apply_theme(app, "dark")  # or "light"

    window = Window()
    window.showMaximized()
    
    sys.exit(app.exec())

