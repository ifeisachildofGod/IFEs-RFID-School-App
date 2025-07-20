
from typing import Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QApplication, QMainWindow,
    QDialog, QComboBox, QLineEdit
)

import sys
import asyncio
import bluetooth as bt_classic
from bleak import BleakScanner
from PyQt6.QtCore import pyqtSignal
from theme.theme import THEME_MANAGER
from PyQt6.QtGui import QAction, QIntValidator
from serial.tools.list_ports import comports

from communication import *
from models.data_models import *
from models.object_models import *
from widgets.base_widgets import *
from widgets.section_widgets import *

class SetupScreen(QDialog):
    update_signal = pyqtSignal(dict, list)
    
    def __init__(self, parent: 'Window'):
        super().__init__(parent=parent)
        
        self.setFocus()
        self.setModal(True)
        self.setWindowTitle("Connection Config")
        self.setFixedWidth(700)
        self.setFixedHeight(500)
        
        self.ble_scanner = BleakScanner()
        
        self.connected = False
        self.data: dict[str, str | int | Literal["bluetooth", "serial"]] = {}
        
        
        
        self.connection_thread = Thread(self.refresh_all)
        self.connection_thread.crashed.connect(parent.connection_error_func)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        
        self.container, self.main_layout = create_widget(layout, QVBoxLayout)
        
        
        serial_widget, serial_layout = create_widget(None, QVBoxLayout)
        serial_widget.setProperty("class", "labeled-widget")
        bluetooth_widget, bluetooth_layout = create_widget(None, QVBoxLayout)
        bluetooth_widget.setProperty("class", "labeled-widget")
        
        self.main_widget = TabViewWidget()
        self.main_widget.add("USB Serial Connection", serial_widget)
        self.main_widget.add("Bluetooth Connection", bluetooth_widget)
        
        _, serial_upper_buttons_layout = create_widget(serial_layout, QHBoxLayout)
        
        serial_refresh_button = QPushButton("Refresh")
        serial_refresh_button.clicked.connect(lambda: self.refresh("ser", serial_refresh_button))
        
        connect_button = QPushButton("Connect")
        connect_button.clicked.connect(self.serial_connect_clicked(-1))
        
        serial_upper_buttons_layout.addWidget(serial_refresh_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        serial_upper_buttons_layout.addWidget(connect_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        
        self.port_options = []
        
        serial_ports_widget, serial_ports_layout = create_widget(None, QHBoxLayout)
        serial_layout.addWidget(serial_ports_widget)
        
        self.port_selector_widget = QComboBox()
        self.port_selector_widget.addItems(self.port_options)
        
        serial_ports_layout.addWidget(QLabel("Ports"))
        serial_ports_layout.addWidget(self.port_selector_widget)
        
        baud_options = ["9600", "119500", "336000", "7844000"]
        
        serial_baud_rate_widget, serial_baud_rate_layout = create_widget(None, QHBoxLayout)
        serial_layout.addWidget(serial_baud_rate_widget, alignment=Qt.AlignmentFlag.AlignTop)
        
        self.baud_rate_selector_widget = QComboBox()
        self.baud_rate_selector_widget.addItems(baud_options)
        
        serial_baud_rate_layout.addWidget(QLabel("Baud rate"))
        serial_baud_rate_layout.addWidget(self.baud_rate_selector_widget)
        
        bluetooth_refesh_button = QPushButton("Refresh")
        bluetooth_refesh_button.clicked.connect(lambda: self.refresh("bt", bluetooth_refesh_button))
        
        bluetooth_layout.addWidget(bluetooth_refesh_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
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
        
        # continue_button = QPushButton("No connection")
        # continue_button.clicked.connect(self.serial_connect_clicked())
        
        # self.main_layout.addWidget(continue_button, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.main_widget)
        
        self.update_signal.connect(self._update_scan_timeout)
        
        self.refresh_tracker = {}
    
    def refresh_all(self):
        while not self.connected:
            self.update_scans(None)
            time.sleep(1)
    
    def refresh(self, refresh_type: str, refresh_button: QPushButton):
        if self.refresh_tracker.get(refresh_type, [True, None])[0]:
            if not self.refresh_tracker.get(refresh_type, False):
                self.refresh_tracker[refresh_type] = [False, None]
            
            self.refresh_tracker[refresh_type][0] = False
            refresh_button.setDisabled(True)
            
            self.refresh_tracker[refresh_type][1] = Thread(lambda: self.update_scans(refresh_type, refresh_type, refresh_button))
            self.refresh_tracker[refresh_type][1].crashed.connect(print)
            self.refresh_tracker[refresh_type][1].start()
    
    def exec(self):
        # self.update_scans(None)
        return super().exec()
    
    def _update_scan_timeout(self, data: dict[str, list[tuple[str, str]] | list[str]], args: list):
        if not args:
            refresh_type = None
            load_spinner = None
        else:
            refresh_type, refresh_button = args
        
        if data.get("ser", None) is not None and self.port_options != data["ser"]:
            self.port_options = data["ser"]
            
            for _ in range(len(self.port_selector_widget)):
                self.port_selector_widget.removeItem(0)
            
            if self.port_selector_widget.currentText() in self.port_options:
                self.port_options.insert(0, self.port_options.pop(self.port_options.index(self.port_selector_widget.currentText())))
            
            self.port_selector_widget.addItems(self.port_options)
            if self.port_options:
                self.port_selector_widget.setCurrentIndex(0)
        
        if data.get("bt", None) is not None and dict(self.bluetooth_devices) != dict(data["bt"]):
            for _ in range(len(self.bluetooth_devices)):
                prev_widget = self.bluetooth_devices_layout.itemAt(0).widget()
                self.bluetooth_devices_layout.removeWidget(prev_widget)
                prev_widget.deleteLater()
            
            self.bluetooth_devices = data["bt"]
            
            for index, (addr, name) in enumerate(self.bluetooth_devices):
                self.add_bt_device(name, addr, index)
        
        if refresh_button is not None:
            refresh_button.setDisabled(False)
        if refresh_type is not None:
            self.refresh_tracker[refresh_type][0] = True
    
    def update_scans(self, send_type: str | None = None, *args):
        data = {}
        
        if send_type == "bt" or send_type is None:
            bt_data = bt_classic.discover_devices(lookup_names=True) + [(bl_info.address, bl_info.name) for bl_info in asyncio.run(self.ble_scanner.discover())]
            data["bt"] = bt_data
        elif send_type == "ser" or send_type is None:
            ser_data = [port.name for port in comports()]
            data["ser"] = ser_data
        
        self.update_signal.emit(data, args)
    
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
    
    def serial_connect_clicked(self, a0: int):
        def func():
            self.connected = True
            
            if a0 == -1:
                self.data["connection-type"] = "serial"
                self.data["port"] = self.port_selector_widget.currentText()
                self.data["baud_rate"] = int(self.baud_rate_selector_widget.currentText())
            elif isinstance(a0, int) and a0 >= 0:
                self.data["connection-type"] = "bluetooth"
                self.data["port"] = int(self.bt_port_edit.text())
                self.data["addr"] = self.bluetooth_devices[a0][1]
            
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
            
        return super().closeEvent(a0)

class Window(QMainWindow):
    comm_signal = pyqtSignal(dict)
    connection_changed = pyqtSignal(bool)
    
    def __init__(self) -> None:
        super().__init__()
        
        self.connection_set_up_screen = SetupScreen(self)
        self.target_connector = BaseCommSystem(CommDevice(LiveData(self.comm_signal), self.connection_changed, "", None, None), self.connection_error_func)
        
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
        
        # Create stacked widget for content
        staff_widget = TabViewWidget("vertical")
        staff_widget.add("Attendance", AttendanceWidget(data, self.target_connector))
        staff_widget.add("Teachers", TeacherEditorWidget(data, self.target_connector, staff_widget.stack, len(staff_widget.tab_buttons), 5, 6))
        staff_widget.add("Prefects", PrefectEditorWidget(data, self.target_connector, staff_widget.stack, len(staff_widget.tab_buttons), 5, 6))
        staff_widget.add("Attendance Chart", AttendanceBarWidget(data))
        staff_widget.add("Punctuality Graph", PunctualityGraphWidget(data))
        staff_widget.stack.addWidget(CardScanScreenWidget(self.target_connector, staff_widget.stack))
        staff_widget.stack.addWidget(StaffDataWidget(data, staff_widget.stack))
        
        
        gas_widget = SensorWidget(Sensor(SensorMeta("Gas", "Flying fish", "13.1.0.1", "Arduino inc"), "img.png", self.target_connector))
        flame_widget = SensorWidget(Sensor(SensorMeta("Fire", "Fire free", "10.0.0.1", "Arduino inc"), "img.png", self.target_connector))
        
        safety_widget, safety_layout = create_scrollable_widget(None, QVBoxLayout)
        
        safety_layout.addWidget(gas_widget)
        safety_layout.addWidget(flame_widget)
        
        main_screen_widget = TabViewWidget()
        main_screen_widget.add("Staff", staff_widget)
        main_screen_widget.add("Security", UltrasonicSonarWidget(Sensor(SensorMeta("Ultrasonic", "Floating bird", "8.9.1", "Arduino inc"), "img.png", self.target_connector)), lambda _: (self.target_connector.send_message("SECURITY") if self.target_connector.connected else ()))
        main_screen_widget.add("Safety", safety_widget, lambda _: (self.target_connector.send_message("SAFETY") if self.target_connector.connected else ()))
        
        main_layout.addWidget(main_screen_widget)
        
        self.setCentralWidget(container)
    
    def activate_connection_screen(self):
        self.connection_set_up_screen.data = {}
        
        self.connection_set_up_screen.exec()
        
        self.target_connector.device.port = self.connection_set_up_screen.data.get("port", "")
        self.target_connector.device.addr = self.connection_set_up_screen.data.get("addr", None)
        self.target_connector.device.baud_rate = self.connection_set_up_screen.data.get("baud_rate", None)
        
        if self.connection_set_up_screen.data.get("connection-type", None) is not None:
            self.target_connector.set_bluetooth(self.connection_set_up_screen.data["connection-type"] == "bluetooth")
            self.target_connector.set_serial(self.connection_set_up_screen.data["connection-type"] == "serial")
            
            self.target_connector.start_connection()
    
    def connection_error_func(self, e: Exception):
        self.target_connector.stop_connection()
        self.connection_set_up_screen.connected = False
        self.connection_set_up_screen.data = {}
        
        QMessageBox.warning(self, "Connection Error", str(e))
        
        self.activate_connection_screen()
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("File") #type: ignore
        connection_menu = menubar.addMenu("Connection") #type: ignore
        
        # Add File Actions
        new_action = QAction("New", self)
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        save_as_action = QAction("Save_as", self)
        exit_action = QAction("Exit", self)
        
        set_connection = QAction("Set", self)
        break_connection = QAction("Break", self)
        
        new_action.setShortcut("Ctrl+N")
        open_action.setShortcut("Ctrl+O")
        save_action.setShortcut("Ctrl+S")
        save_as_action.setShortcut("Ctrl+Shift+S")
        
        set_connection.setShortcut("Ctrl+F")
        break_connection.setShortcut("Ctrl+Shift+F")
        
        exit_action.triggered.connect(self.close)
        set_connection.triggered.connect(self.activate_connection_screen)
        
        def _break_connection(): self.target_connector.connected = False
        break_connection.triggered.connect(_break_connection)
        
        file_menu.addActions([new_action, open_action, save_action, save_as_action, exit_action]) #type: ignore
        connection_menu.addActions([set_connection, break_connection])
    
    # def closeEvent(self, a0):
    #     response = QMessageBox.question(self, "Quit", "Are you sure you want to quit",
    #     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
    #     if response == QMessageBox.StandardButton.Yes:
    #         a0.accept()
    #     else:
    #         a0.ignore()
    #         return
        
    #     return super().closeEvent(a0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    THEME_MANAGER.apply_theme(app, "dark")  # or "light"

    window = Window()
    window.showMaximized()
    
    sys.exit(app.exec())

