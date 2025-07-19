
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QApplication, QMainWindow,
    QDialog, QComboBox, QLineEdit
)

import sys
import asyncio
import bluetooth
from bleak import BleakScanner
from PyQt6.QtCore import pyqtSignal
from theme.theme import THEME_MANAGER
from PyQt6.QtGui import QAction, QIntValidator

from communication import *
from models.data_models import *
from models.object_models import *
from widgets.base_widgets import *
from widgets.section_widgets import *


class SetupScreen(QDialog):
    update_signal = pyqtSignal(list)
    
    def __init__(self, parent: 'Window'):
        super().__init__(parent=parent)
        
        self.setFocus()
        self.setModal(True)
        self.setWindowTitle("Connection Config")
        self.setFixedWidth(700)
        self.setFixedHeight(500)
        
        self.ble_scanner = BleakScanner()
        
        self.connected = False
        self.data: dict[str, str | int | type[DirectSerial] | type[Bluetooth]] = {}
        
        
        self.connection_thread = Thread(self.update_scans)
        self.connection_thread.crashed.connect(parent.connection_error_func)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.container, self.main_layout = create_widget(layout, QVBoxLayout)
        
        
        serial_widget, serial_layout = create_widget(None, QVBoxLayout)
        bluetooth_widget, bluetooth_layout = create_widget(None, QVBoxLayout)
        
        self.main_widget = TabViewWidget()
        self.main_widget.add("USB Serial Connection", serial_widget)
        self.main_widget.add("Bluetooth Connection", bluetooth_widget)
        
        
        connect_button = QPushButton("Connect")
        connect_button.clicked.connect(self.serial_connect_clicked(-1))
        
        serial_layout.addWidget(connect_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        
        port_options = ["COM12", "COM7", "COM8"]
        # port_options = ["COM3", "COM12 (Elecrow CrowPanel 7.0P)", "COM5", "COM12"]
        
        _, serial_ports_layout = create_widget(serial_layout, QHBoxLayout)
        
        self.port_selector_widget = QComboBox()
        self.port_selector_widget.addItems(port_options)
        
        serial_ports_layout.addWidget(QLabel("Ports"))
        serial_ports_layout.addWidget(self.port_selector_widget)
        
        baud_options = ["9600", "119500", "336000", "7844000"]
        
        _, serial_baud_rate_layout = create_widget(serial_layout, QHBoxLayout)
        
        self.baud_rate_selector_widget = QComboBox()
        self.baud_rate_selector_widget.addItems(baud_options)
        
        serial_baud_rate_layout.addWidget(QLabel("Baud rate"))
        serial_baud_rate_layout.addWidget(self.baud_rate_selector_widget)
        
        self.bluetooth_devices = []
        
        bluetooth_devices_widget, self.bluetooth_devices_layout = create_scrollable_widget(None, QVBoxLayout)
        
        for index, (addr, name) in enumerate(self.bluetooth_devices):
            self.add_bt_device(name, addr, index)
        
        self.bt_port_edit = QLineEdit()
        self.bt_port_edit.setValidator(QIntValidator())
        
        bt_port_edit_widget, bt_port_edit_layout = create_widget(bluetooth_layout, QHBoxLayout)
        
        bt_port_edit_layout.addWidget(QLabel("Port"))
        bt_port_edit_layout.addWidget(self.bt_port_edit)
        
        bluetooth_layout.addWidget(LabeledField("Bluetooth Devices", bluetooth_devices_widget, height_size_policy=QSizePolicy.Policy.Minimum))
        bluetooth_layout.addWidget(bt_port_edit_widget, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        
        continue_button = QPushButton("No connection")
        continue_button.clicked.connect(self.serial_connect_clicked())
        
        self.main_layout.addWidget(continue_button, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.main_widget)
        
        self.update_signal.connect(self._update_scans)
        self.connection_thread.start()
    
    def _update_scans(self, data: list):
        if dict(self.bluetooth_devices) != dict(data):
            for index in range(len(self.bluetooth_devices)):
                prev_widget = self.bluetooth_devices_layout.itemAt(0).widget()
                self.bluetooth_devices_layout.removeWidget(prev_widget)
                prev_widget.deleteLater()
            
            self.bluetooth_devices = data
            
            for index, (addr, name) in enumerate(self.bluetooth_devices):
                self.add_bt_device(name, addr, index)
    
    def update_scans(self):
        while not self.connected:
            bt_data = bluetooth.discover_devices(lookup_names=True) + [(bl_info.address, bl_info.name) for bl_info in asyncio.run(self.ble_scanner.discover())]
            
            self.update_signal.emit(bt_data)
            
            time.sleep(1)
    
    def add_bt_device(self, name: str, addr: str, index: int):
        connect_button = QPushButton("Connect")
        connect_button.clicked.connect(self.serial_connect_clicked(index))
        
        _, bt_device_layout = create_widget(self.bluetooth_devices_layout, QHBoxLayout)
            
        _, info_layout = create_widget(bt_device_layout, QVBoxLayout)
        
        name_label = QLabel(name)
        name_label.setStyleSheet("font-size: 30px; font-weight: 900;")
        addr_label = QLabel(addr)
        addr_label.setStyleSheet("font-size: 20px; font-weight: 100;")
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(addr_label)
        
        bt_device_layout.addWidget(connect_button, alignment=Qt.AlignmentFlag.AlignRight)
    
    def serial_connect_clicked(self, a0: int | None = None):
        def func():
            self.connected = True
            
            if a0 == -1:
                self.data["type"] = DirectSerial
                self.data["port"] = self.port_selector_widget.currentText()
                self.data["baud_rate"] = int(self.baud_rate_selector_widget.currentText())
            elif isinstance(a0, int) and a0 >= 0:
                self.data["type"] = Bluetooth
                self.data["port"] = int(self.bt_port_edit.text())
                self.data["addr"] = self.bluetooth_devices[a0][1]
            elif a0 is None:
                self.connected = False
                
                self.data["type"] = None
                self.data["port"] = None
                self.data["addr"] = None
            
            self.close()
        
        return func
    
    def closeEvent(self, a0):
        if self.connected:
            response = QMessageBox.question(self, "Connection mode", "Are you want to continue with these settings",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if response == QMessageBox.StandardButton.Yes:
                a0.accept()
            else:
                self.connected = False
                self.data = {}
                
                a0.ignore()
                return
        elif self.data:
            response = QMessageBox.question(self, "Data viewer mode", "Are you sure you want to just view the data",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if response == QMessageBox.StandardButton.Yes:
                a0.accept()
            else:
                a0.ignore()
                return
        else:
            response = QMessageBox.question(self, "Quit", "Are you sure you want to quit",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if response == QMessageBox.StandardButton.Yes:
                a0.accept()
            else:
                a0.ignore()
                return
            
        return super().closeEvent(a0)

class Window(QMainWindow):
    bt_signal = pyqtSignal(dict)
    
    def __init__(self) -> None:
        super().__init__()
        
        self.connection_set_up_screen = SetupScreen(self)
        self.activate_connection_screen()
        
        self.setWindowTitle(f"IFEs Attendance Tracker")
        
        self.create_menu_bar()
        
        # Create main container
        container = QWidget()
        main_layout = QHBoxLayout()
        
        container.setLayout(main_layout)
        
        # Create sidebar layout
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(0)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        
        data = AppData(
            Time(7, 00, 00),
            Time(8, 00, 00),
            
            (AttendanceEntry(Time(7, 00, 00), "Monday", 1, "January", 2025), AttendanceEntry(Time(7, 00, 00), "Monday", 1, "January", 2025)),
            (AttendanceEntry(Time(7, 00, 00), "Monday", 1, "January", 2025), AttendanceEntry(Time(7, 00, 00), "Monday", 1, "January", 2025)),
            
            [],
            
            {"t_id1": Teacher("t_id1", None, CharacterName("Emily", "Mbeke", "Chinweotito", "Mbeke"), Department("d_id1", "Humanities"), [Subject("s_id1", "Civic Education", Class("c_id1", "A", "SS3", "SS3 A"), [("Friday", 2), ("Friday", 3)])], "img.png", [])},
            {"p_id1": Prefect("p_id1", None, CharacterName("Eze", "Emmanuel", "Udochukwu", "Emma"), "Parade Commander", Class("c_id1", "A", "SS3", "SS3 A"), "img.png", {"Friday": ["Morning", "Parade"]}, [])}
        )
        
        if self.connection_set_up_screen.data["type"] is not None:
            target_connector = self.connection_set_up_screen.data["type"](CommDevice(LiveData(self.bt_signal), self.connection_set_up_screen.data["port"], self.connection_set_up_screen.data.get("addr", None), self.connection_set_up_screen.data.get("baud_rate", None)), self.connection_error_func)
            target_connector.start_connection()
        else:
            target_connector = BaseCommSystem(CommDevice(LiveData(self.bt_signal), self.connection_set_up_screen.data["port"], self.connection_set_up_screen.data.get("addr", None), self.connection_set_up_screen.data.get("baud_rate", None)), self.connection_error_func)
        
        # Create stacked widget for content
        staff_widget = TabViewWidget("vertical")
        staff_widget.add("Attendance", AttendanceWidget(data, target_connector))
        staff_widget.add("Teachers", TeacherEditorWidget(data, target_connector, staff_widget.stack, len(staff_widget.tab_buttons), 5, 6))
        staff_widget.add("Prefects", PrefectEditorWidget(data, target_connector, staff_widget.stack, len(staff_widget.tab_buttons), 5, 6))
        staff_widget.add("Attendance Chart", AttendanceBarWidget(data))
        staff_widget.add("Punctuality Graph", PunctualityGraphWidget(data))
        staff_widget.stack.addWidget(CardScanScreenWidget(target_connector, staff_widget.stack))
        staff_widget.stack.addWidget(StaffDataWidget(data, staff_widget.stack))
        
        
        gas_widget = SensorWidget(Sensor(SensorMeta("Gas", "Flying fish", "13.1.0.1", "Arduino inc"), "img.png", target_connector))
        flame_widget = SensorWidget(Sensor(SensorMeta("Fire", "Fire free", "10.0.0.1", "Arduino inc"), "img.png", target_connector))
        
        safety_widget, safety_layout = create_scrollable_widget(None, QVBoxLayout)
        
        safety_layout.addWidget(gas_widget)
        safety_layout.addWidget(flame_widget)
        
        main_screen_widget = TabViewWidget()
        main_screen_widget.add("Staff", staff_widget)
        main_screen_widget.add("Security", UltrasonicSonarWidget(Sensor(SensorMeta("Ultrasonic", "Floating bird", "8.9.1", "Arduino inc"), "img.png", target_connector)), lambda _: (target_connector.send_message("SECURITY") if target_connector.connected else ()))
        main_screen_widget.add("Safety", safety_widget, lambda _: (target_connector.send_message("SAFETY") if target_connector.connected else ()))
        
        main_layout.addWidget(main_screen_widget)
        
        self.setCentralWidget(container)
    
    def activate_connection_screen(self):
        self.connection_set_up_screen.data = {}
        
        self.connection_set_up_screen.exec()
        
        if not self.connection_set_up_screen.data:
            exit(0)
    
    def connection_error_func(self, e):
        self.connection_set_up_screen.connected = False
        self.connection_set_up_screen.data = {}
        
        QMessageBox.warning(self, "Connection Error", str(e))
        
        self.activate_connection_screen()
    
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
    
    def closeEvent(self, a0):
        response = QMessageBox.question(self, "Quit", "Are you sure you want to quit",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if response == QMessageBox.StandardButton.Yes:
            a0.accept()
        else:
            a0.ignore()
            return
        
        return super().closeEvent(a0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    THEME_MANAGER.apply_theme(app, "dark")  # or "light"

    window = Window()
    window.showMaximized()
    
    sys.exit(app.exec())

