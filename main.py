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
from widgets.base_widgets import *
from widgets.section_widgets import *
from models.data_models import *
from models.object_models import *
from PyQt6.QtGui import QDrag, QDragEnterEvent, QDragMoveEvent, QDropEvent, QAction, QImage
from PyQt6.QtCore import Qt, QMimeData, QThread, QTimer, pyqtSignal
from theme.theme import ThemeManager, THEME_MANAGER


addr = "00:19:08:36:3F:5C"
from PyQt6.QtWidgets import QWidget, QPushButton, QStackedLayout, QHBoxLayout, QVBoxLayout, QSizePolicy, QFrame
from PyQt6.QtCore import Qt


class Window(QMainWindow):
    bt_signal = pyqtSignal(dict)
    
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
        
        data = AppData(
            Time(7, 00, 00),
            Time(8, 00, 00),
            
            (AttendanceEntry(Time(7, 00, 00), "Monday", 1, "January", 2025), AttendanceEntry(Time(7, 00, 00), "Monday", 1, "January", 2025)),
            (AttendanceEntry(Time(7, 00, 00), "Monday", 1, "January", 2025), AttendanceEntry(Time(7, 00, 00), "Monday", 1, "January", 2025)),
            
            [],
            
            {},
            {}
        )
        
        bt_data = LiveData(self.bt_signal)
        
        # Create stacked widget for content
        
        staff_widget = TabViewWidget("vertical")
        staff_widget.add("Attendance", AttendanceWidget(data, bt_data))
        staff_widget.add("Attendance Graph", AttendanceBarWidget(data))
        staff_widget.add("Punctuality Graph", PunctualityGraphWidget(data))
        staff_widget.add("Prefect Editor", PrefectEditorWidget(data, staff_widget.stack, len(staff_widget.tab_buttons), 5, 6))
        staff_widget.add("Teacher Editor", TeacherEditorWidget(data, staff_widget.stack, len(staff_widget.tab_buttons), 5, 6))
        staff_widget.stack.addWidget(CardScanScreenWidget(bt_data, staff_widget.stack))
        staff_widget.stack.addWidget(StaffDataWidget(bt_data, staff_widget.stack))
        
        main_screen_widget = TabViewWidget()
        main_screen_widget.add("Staff", staff_widget)
        main_screen_widget.add("Security", UltrasonicSonarWidget(Sensor(SensorMeta("Ultrasonic", "Floating bird", "8.9.1", "Arduino inc"), "img.png")))
        main_screen_widget.add("Safety", safety_widget)
        
        main_layout.addWidget(main_screen_widget)
        
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

