
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QApplication, QMainWindow, QToolBar
)

import sys
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal
from bt import BT_Device, Bluetooth
from theme.theme import THEME_MANAGER

from models.data_models import *
from models.object_models import *
from widgets.base_widgets import *
from widgets.section_widgets import *


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
        
        safety_layout.addWidget(gas_widget)
        safety_layout.addWidget(flame_widget)
        
        data = AppData(
            Time(7, 00, 00),
            Time(8, 00, 00),
            
            (AttendanceEntry(Time(7, 00, 00), "Monday", 1, "January", 2025), AttendanceEntry(Time(7, 00, 00), "Monday", 1, "January", 2025)),
            (AttendanceEntry(Time(7, 00, 00), "Monday", 1, "January", 2025), AttendanceEntry(Time(7, 00, 00), "Monday", 1, "January", 2025)),
            
            [],
            
            {"t_id1": Teacher("t_id1", None, CharacterName("Emily", "Mbeke", "Chinweotito", "Mbeke"), Department("d_id1", "Humanities"), [Subject("s_id1", "Civic Education", Class("c_id1", "A", "SS3", "SS3 A"), [("Friday", 2), ("Friday", 3)])], "img.png", {})},
            {"p_id1": Prefect("p_id1", "iud_1", CharacterName("Eze", "Emmanuel", "Udochukwu", "Emma"), "Parade Commander", Class("c_id1", "A", "SS3", "SS3 A"), "img.png", {"Friday": ["Morning", "Parade"]}, {})}
        )
        
        bluetooth = Bluetooth(BT_Device("IFECHUKWU", "00:19:08:36:3F:5C", LiveData(self.bt_signal)))
        
        # Create stacked widget for content
        staff_widget = TabViewWidget("vertical")
        staff_widget.add("Attendance", AttendanceWidget(data, bluetooth.device.live_data))
        staff_widget.add("Attendance Graph", AttendanceBarWidget(data))
        staff_widget.add("Punctuality Graph", PunctualityGraphWidget(data))
        staff_widget.add("Prefect Editor", PrefectEditorWidget(data, bluetooth, staff_widget.stack, len(staff_widget.tab_buttons), 5, 6))
        staff_widget.add("Teacher Editor", TeacherEditorWidget(data, bluetooth, staff_widget.stack, len(staff_widget.tab_buttons), 5, 6))
        staff_widget.stack.addWidget(CardScanScreenWidget(bluetooth.device.live_data, staff_widget.stack))
        staff_widget.stack.addWidget(StaffDataWidget(data, staff_widget.stack))
        
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

