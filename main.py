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
    QStackedWidget, QMessageBox, QFileDialog, QToolBar
)
from app_sections import SchoolManager
from PyQt6.QtGui import QDrag, QDragEnterEvent, QDragMoveEvent, QDropEvent, QAction, QImage
from PyQt6.QtCore import Qt, QMimeData, QThread, QTimer

from theme import ThemeManager, THEME_MANAGER


addr = "00:19:08:36:3F:5C"

class TabViewWidget(QWidget):
    def __init__(self, tab_widget_mapping: dict[str, QWidget], bar_orientation: Literal["vertical", "horizontal"]):
        super().__init__()
        layout_type = QHBoxLayout if bar_orientation == "horizontal" else QVBoxLayout
        
        layout = layout_type()
        self.setLayout(layout)
        
        assert bar_orientation in ("vertical", "horizontal"), f"Invalid orientation: {bar_orientation}"
        
        tab_widget = QWidget()
        tab_layout = layout_type()
        tab_widget.setLayout(tab_layout)
        
        self.tab_widget_mapping = tab_widget_mapping
        self.bar_orientation = bar_orientation
        
        stack = QStackedWidget()
        
        for tab_name, widget in tab_widget_mapping.items():
            tab_button = QPushButton(tab_name)
            tab_button.clicked.connect(self.make_tab_clicked_func())
            tab_button.setProperty("class", "HorizontalTab" if bar_orientation == "horizontal" else "VerticalTab")
            
            tab_layout.addWidget(tab_button)
            stack.addWidget(widget)
        
        layout.addWidget(tab_widget)
        layout.addWidget(stack)
    
    def make_tab_clicked_func(self, index: int):
        def func():
            pass
        
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
        
        # Create stacked widget for content
        stack = QStackedWidget()
        
        self.school_manager = SchoolManager()
        
        stack.addWidget(self.school_manager)
        
        # Add widgets to main layout
        main_layout.addWidget(stack)
        
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

