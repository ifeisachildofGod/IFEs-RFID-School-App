
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QScrollArea, QLabel,
    QSizePolicy, QStackedWidget, QSlider,
    QCheckBox
)

import time
from bt import Bluetooth
from typing import Literal
from PyQt6.QtCore import Qt
from matplotlib.cbook import flatten
from theme.theme import THEME_MANAGER
from matplotlib.colors import get_named_colors_mapping

from others import *
from models.data_models import *
from widgets.base_widgets import *
from widgets.section_sub_widgets import *
from models.collection_data_models import *




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
        
        if self.bar_orientation == "vertical":
            self.tab_layout.addStretch()
        
        self.setContentsMargins(0, 0, 0, 0)
        tab_widget.setContentsMargins(0, 0, 0, 0)
        self.stack.setContentsMargins(0, 0, 0, 0)
        
        layout.addWidget(tab_widget)
        layout.addWidget(self.stack)
        
        main_layout.addWidget(container)
    
    def add(self, tab_name: str, widget: QWidget, func: Callable[[int, ], None] = None):
        tab_button = QPushButton(tab_name)
        tab_button.setCheckable(True)
        tab_button.clicked.connect(self._make_tab_clicked_func(len(self.tab_buttons), func))
        tab_button.setProperty("class", "HorizontalTab" if self.bar_orientation == "horizontal" else "VerticalTab")
        tab_button.setContentsMargins(0, 0, 0, 0)
        
        self.tab_layout.insertWidget(len(self.tab_buttons), tab_button)
        self.stack.insertWidget(len(self.tab_buttons), widget)
        widget.setContentsMargins(0, 0, 0, 0)
        
        self.tab_buttons.append(tab_button)
        
        self.tab_buttons[0].click()
    
    def _make_tab_clicked_func(self, index: int, clicked_func: Callable[[int, ], None] | None):
        def func():
            if clicked_func is not None:
                clicked_func(index)
            
            self.stack.setCurrentIndex(index)
            
            for i, button in enumerate(self.tab_buttons):
                if i != index:
                    button.setChecked(False)
        
        return func



class BaseListWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        scroll_widget = QScrollArea()
        scroll_widget.setWidgetResizable(True)
        
        widget = QWidget()
        scroll_widget.setWidget(widget)
        self.main_layout = QVBoxLayout(widget)
        
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        
        layout.addWidget(scroll_widget)


class AttendanceWidget(BaseListWidget):
    def __init__(self, data: AppData, bluetooth: Bluetooth):
        super().__init__()
        
        self.data = data
        self.attendance_dict = {}
        
        _, cit_layout = create_widget(self.main_layout, QHBoxLayout)
        
        cit_teacher_widget, cit_teacher_layout = create_widget(cit_layout, QHBoxLayout)
        
        cit_teacher_layout.addWidget(LabeledField("Hour", QLabel(("0" if self.data.teacher_cit.hour < 10 else "") + str(self.data.teacher_cit.hour))))
        cit_teacher_layout.addWidget(LabeledField("Minutes", QLabel(("0" if self.data.teacher_cit.min < 10 else "") + str(self.data.teacher_cit.min))))
        cit_teacher_layout.addWidget(LabeledField("Seconds", QLabel(("0" if self.data.teacher_cit.sec < 10 else "") + str(self.data.teacher_cit.sec))))
        
        cit_layout.addWidget(LabeledField("Teacher Check-in Time", cit_teacher_widget, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
        
        cit_prefect_widget, cit_prefect_layout = create_widget(cit_layout, QHBoxLayout)
        
        cit_prefect_layout.addWidget(LabeledField("Hour", QLabel(("0" if self.data.prefect_cit.hour < 10 else "") + str(self.data.prefect_cit.hour))))
        cit_prefect_layout.addWidget(LabeledField("Minutes", QLabel(("0" if self.data.prefect_cit.min < 10 else "") + str(self.data.prefect_cit.min))))
        cit_prefect_layout.addWidget(LabeledField("Seconds", QLabel(("0" if self.data.prefect_cit.sec < 10 else "") + str(self.data.prefect_cit.sec))))
        
        cit_layout.addWidget(LabeledField("Prefect Check-in Time", cit_prefect_widget, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
        
        _, self.attendance_layout = create_widget(self.main_layout, QVBoxLayout)
        
        for attendance in self.data.attendance_data:
            self.add_attendance_log(attendance)
        
        self.main_layout.addStretch()
        
        bluetooth.set_data_point("IUD", self.add_new_attendance_log)
    
    def add_attendance_log(self, attendance_entry: AttendanceEntry):
        if isinstance(attendance_entry.staff, Teacher):
            widget = AttendanceTeacherWidget(attendance_entry)
        elif isinstance(attendance_entry.staff, Prefect):
            widget = AttendancePrefectWidget(attendance_entry)
        else:
            raise TypeError(f"Type: {type(attendance_entry.staff)} is not supported")
        
        self.attendance_layout.addWidget(widget)
    
    def add_new_attendance_log(self, IUD: str):
        staff = next((prefect for _, prefect in self.data.prefects.items() if prefect.IUD == IUD), None)
        if staff is None:
            staff = next((teacher for _, teacher in self.data.teachers.items() if teacher.IUD == IUD))
        
        day, month, date, t, year = time.ctime().split()
        hour, min, sec = t.split(":")
        
        day = next((dotw for dotw in DAYS_OF_THE_WEEK if day in dotw))
        month = next((moty for moty in MONTHS_OF_THE_YEAR if month in moty))
        
        entry = AttendanceEntry(Time(int(hour), int(min), int(sec)), day, int(date), month, int(year), staff)
        
        self.add_attendance_log(entry)
        
        staff.attendance.append(entry)
        self.data.attendance_data.append(entry)


class PrefectEditorWidget(BaseListWidget):
    def __init__(self, data: AppData, bluetooth: Bluetooth, parent_widget: QStackedWidget, curr_index: int, card_scanner_index: int, staff_data_index: int):
        super().__init__()
        
        for _, prefect in data.prefects.items():
            self.main_layout.addWidget(EditorPrefectWidget(data, prefect, bluetooth, parent_widget, curr_index, card_scanner_index, staff_data_index))
        
        self.main_layout.addStretch()

class TeacherEditorWidget(BaseListWidget):
    def __init__(self, data: AppData, bluetooth: Bluetooth, parent_widget: QStackedWidget, curr_index: int, card_scanner_index: int, staff_data_index: int):
        super().__init__()
        
        for _, teacher in data.teachers.items():
            self.main_layout.addWidget(EditorTeacherWidget(data, teacher, bluetooth, parent_widget, curr_index, card_scanner_index, staff_data_index))
        
        self.main_layout.addStretch()


class AttendanceBarWidget(BaseListWidget):
    def __init__(self, data: AppData):
        super().__init__()
        
        teacher_data: dict[str, tuple[str, tuple[list[str], list[int]]]] = {}
        
        prefect_names = []
        prefects_attendance_data = []
        
        prefect_interval = get_attendance_time_interval(*data.prefect_timeline_dates)
        teacher_interval = get_attendance_time_interval(*data.teacher_timeline_dates)
        
        for staff_attendance_data in data.attendance_data:
            if isinstance(staff_attendance_data.staff, Prefect):
                percentage_attendance = self.get_percentage_attendance(staff_attendance_data.staff.attendance, list(staff_attendance_data.staff.duties.keys()), prefect_interval)
                
                prefect_names.append(staff_attendance_data.staff.name)
                prefects_attendance_data.append(percentage_attendance)
            elif isinstance(staff_attendance_data.staff, Teacher):
                days_tba = list(set(flatten([[day for day, _ in s.periods] for s in staff_attendance_data.staff.subjects])))
                
                percentage_attendance = self.get_percentage_attendance(staff_attendance_data.staff.attendance, days_tba, teacher_interval)
                
                if staff_attendance_data.staff.department.id in teacher_data:
                    teacher_data[staff_attendance_data.staff.department.id][1][0].append(staff_attendance_data.staff.name)
                    teacher_data[staff_attendance_data.staff.department.id][1][1].append(percentage_attendance)
                else:
                    teacher_data[staff_attendance_data.staff.department.id] = (staff_attendance_data.staff.department.name, [(staff_attendance_data.staff.name), percentage_attendance])
        
        if prefects_attendance_data:
            prefect_info_widget = BarWidget("Cummulative Prefect Attendance", "Prefect Names", "Yearly Attendance (%)")
            prefect_info_widget.add_data("Prefects", THEME_MANAGER.get_current_palette()["prefect"], (prefect_names, prefects_attendance_data))
            
            self.main_layout.addWidget(LabeledField("Prefect Attendance", prefect_info_widget, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        else:
            label = QLabel("No Prefect Attendance Data")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.main_layout.addWidget(LabeledField("Prefect Attendance", label, height_size_policy=QSizePolicy.Policy.Maximum))
        
        dtd_widget, dtd_layout = create_widget(None, QVBoxLayout)
        # dtd_widget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        
        if teacher_data:
            for index, (_, (name, data)) in enumerate(teacher_data.items()):
                widget = BarWidget(f"Cummulative {name} Attendance", f"{name} Department Teachers", "Yearly Attendance (%)")
                widget.add_data(name, list(get_named_colors_mapping().values())[index], data)
                
                dtd_layout.addWidget(widget)
            
            self.main_layout.addWidget(LabeledField("Departmental Attendance", dtd_widget, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        else:
            label = QLabel("No Teacher Attendance Data")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.main_layout.addWidget(LabeledField("Teacher Attendance", label, height_size_policy=QSizePolicy.Policy.Maximum), alignment=Qt.AlignmentFlag.AlignTop)
    
    def get_percentage_attendance(self, attendance: list[AttendanceEntry], valid_attendance_days: list[str], interval: tuple[int, int]):
        remainder_days = sum([day in valid_attendance_days for day in DAYS_OF_THE_WEEK[:interval[1] + 1]])
        max_attendance = (len(valid_attendance_days) * interval[0]) + remainder_days
        
        percentage_attendance = len(attendance) * 100 / max_attendance
        
        return percentage_attendance

class PunctualityGraphWidget(BaseListWidget):
    def __init__(self, data: AppData):
        super().__init__()
        
        self.data = data
        
        teacher_data = {}
        prefects_data = {}
        
        for staff_attendance_data in self.data.attendance_data:
            if isinstance(staff_attendance_data.staff, Prefect):
                prefects_data[staff_attendance_data.staff.IUD] = self.get_punctuality_data(staff_attendance_data.staff)
            elif isinstance(staff_attendance_data.staff, Teacher):
                teacher_data[staff_attendance_data.staff.department.id][1][staff_attendance_data.staff.IUD] = self.get_punctuality_data(staff_attendance_data.staff)
        
        # sub_data = {
        #     "prefect_id 1": ("Emma", [0, 0, 0, 1, 1, 2, 2, -1, -1, -3, 0, -2, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3]),
        #     "prefect_id 2": ("Bambi", [0, 0, 0, -2, 1, 2, 2, 0, -1, -3, 0, -2, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3]),
        #     "prefect_id 3": ("Mikalele", [0, 0, -1, 0, 1, 1, 2, 0, -1, -3, 0, -2, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3]),
        #     "prefect_id 4": ("Jesse", [0, 0, 0, 1, 1, 2, 3, 0, -1, -3, 0, -2, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3]),
        #     "prefect_id 5": ("Tumbum", [0, 0, 0, 3, 1, 2, 0, 0, -1, -3, 0, -2, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3]),
        # }
        
        if prefects_data:
            prefect_info_widget = GraphWidget("Prefects Punctuality Graph", "Time Interval (Weeks)", "Punctuality (Hours)")
            
            for index, (_, (name, prefect_data)) in enumerate(prefects_data.items()):
                prefect_info_widget.plot([i + 1 for i in range(len(prefect_data))], prefect_data, label=name, marker='o', color=list(get_named_colors_mapping().values())[index])
            
            self.main_layout.addWidget(LabeledField("Prefect Punctuality", prefect_info_widget))
        else:
            label = QLabel("No Prefect Punctuality Data")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.main_layout.addWidget(LabeledField("Prefect Punctuality", label, height_size_policy=QSizePolicy.Policy.Maximum))
        
        dtd_widget, dtd_layout = create_widget(None, QVBoxLayout)
        
        if teacher_data:
            for _, (dep_name, dep_data) in teacher_data.items():
                dep_info_widget = GraphWidget(f"{dep_name} Department Punctuality Graph", "Time Interval (Weeks)", "Punctuality (Hours)")
                
                for index, (_, (name, info)) in enumerate(dep_data.items()):
                    dep_info_widget.plot([i + 1 for i in range(len(info))], info, label=name, marker='o', color=list(get_named_colors_mapping().values())[index])
                
                dtd_layout.addWidget(dep_info_widget)
            
            self.main_layout.addWidget(LabeledField("Departmental Punctuality", dtd_widget if teacher_data else QLabel("No Teacher Punctuality Data"), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        else:
            label = QLabel("No Teacher Punctuality Data")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.main_layout.addWidget(LabeledField("Departmental Punctuality", label, height_size_policy=QSizePolicy.Policy.Maximum), alignment=Qt.AlignmentFlag.AlignTop)
    
    def get_punctuality_data(self, staff: Teacher | Prefect):
        prefects_plot_data: list[float] = []
        
        weeks: list[list[Time]] = []
        
        prev_day = DAYS_OF_THE_WEEK[0]
        prev_dt = 1
        
        for attendance in staff.attendance:
            if ((DAYS_OF_THE_WEEK.index(attendance.day) > DAYS_OF_THE_WEEK.index(prev_day)) or
                (prev_dt != attendance.date and
                 DAYS_OF_THE_WEEK.index(attendance.day) == DAYS_OF_THE_WEEK.index(prev_day))
                ):
                weeks.append([attendance.time])
            else:
                weeks[-1].append(attendance.time)
            
            prev_day = attendance.day
            prev_dt = attendance.date
        
        for week_time in weeks:
            weekly_punctuality = sum([(self.data.prefect_cit.hour - t.hour) * 60 + (self.data.prefect_cit.min - t.min) * 60 + (self.data.prefect_cit.sec - t.sec) / 60 for t in week_time])
            prefects_plot_data.append(weekly_punctuality)
        
        return staff.name, prefects_plot_data



class _SensorMetaInfoWidget(QWidget):
    def __init__(self, data: SensorMeta):
        super().__init__()
        self.data = data
        
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        widget_2_1 = QWidget()
        layout_2_1 = QVBoxLayout()
        widget_2_1.setLayout(layout_2_1)
        
        widget_2_1_1 = QWidget()
        layout_2_1_1 = QHBoxLayout()
        widget_2_1_1.setLayout(layout_2_1_1)
        layout_2_1.addWidget(widget_2_1_1)
        
        name_1 = LabeledField("Sensor Name", QLabel(f"{self.data.sensor_type} sensor"))
        name_2 = LabeledField("Model", QLabel(self.data.model))
        name_3 = LabeledField("Version", QLabel(self.data.version))
        
        layout_2_1_1.addWidget(name_1)
        layout_2_1_1.addWidget(name_2)
        layout_2_1_1.addWidget(name_3)
        
        widget_2_1_2 = QWidget()
        layout_2_1_2 = QHBoxLayout()
        widget_2_1_2.setLayout(layout_2_1_2)
        layout_2_1.addWidget(widget_2_1_2)
        
        name_4 = LabeledField("Manufacturer", QLabel(self.data.developer))
        # name_5 = LabeledField("Abbreviation", QLabel(self.data.abrev))
        
        layout_2_1_2.addWidget(name_4, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.main_layout.addWidget(LabeledField("Meta Info", widget_2_1, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))

class SensorWidget(QWidget):
    def __init__(self, sensor: Sensor):
        super().__init__()
        
        self.sensor = sensor
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.container = QWidget()
        
        self.main_layout = QVBoxLayout()
        self.container.setLayout(self.main_layout)
        
        self.labeled_container = LabeledField(self.sensor.meta_data.sensor_type, self.container)
        
        layout.addWidget(self.labeled_container)
        
        widget_1, layout_1 = create_widget(None, QHBoxLayout)
        
        image = Image(self.sensor.img_path, parent=self.container, width=150)
        layout_1.addWidget(image, alignment=Qt.AlignmentFlag.AlignCenter)
        # layout_1.addStretch()
        
        widget_1_2, layout_1_2 = create_widget(None, QHBoxLayout)
        
        widget_1_2_1_1, layout_1_2_1_1 = create_widget(None, QVBoxLayout)
        
        self.reading_slider = QSlider(Qt.Orientation.Horizontal)
        self.sensor.bluetooth.set_data_point(sensor.meta_data.sensor_type, lambda data: self.reading_slider.setValue(data))
        self.reading_slider.setDisabled(True)
        self.reading_slider.setValue(0)
        
        meta_info_widget = _SensorMetaInfoWidget(self.sensor.meta_data)
        layout_1_2.addWidget(meta_info_widget)
        
        safety_reading_slider = QSlider(Qt.Orientation.Horizontal)
        safety_reading_slider.setValue(50)
        
        layout_1_2_1_1.addWidget(LabeledField("Reading", self.reading_slider))
        layout_1_2_1_1.addWidget(LabeledField("Safety Value", safety_reading_slider))
        
        layout_1.addWidget(widget_1_2)
        
        self.main_layout.addWidget(LabeledField("Info", widget_1, height_size_policy=QSizePolicy.Policy.Maximum))
        
        _, layout_2 = create_widget(self.main_layout, QVBoxLayout)
        
        layout_2.addWidget(LabeledField("Live Data", widget_1_2_1_1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
    
    # def reading_value_changed(self):
    #     self.reading_slider.setStyleSheet("")

class UltrasonicSonarWidget(QWidget):
    def __init__(self, sensor: Sensor):
        super().__init__()
        
        self.sonar = sensor
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.container = QWidget()
        
        self.main_layout = QHBoxLayout()
        self.container.setLayout(self.main_layout)
        
        self.labeled_field = LabeledField(self.sonar.meta_data.sensor_type, self.container)
        
        activate_cb = QCheckBox("Activate Sonar")
        activate_cb.clicked.connect(self.toogle_activation_state)
        
        layout.addWidget(activate_cb, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.labeled_field)
        
        ultrasonic_sensor_meta_info_widget, ultrasonic_sensor_meta_info_layout = create_widget(self.main_layout, QVBoxLayout)
        
        ultrasonic_sensor_meta_info_layout.addWidget(Image(self.sonar.img_path, ultrasonic_sensor_meta_info_widget, width=130), alignment=Qt.AlignmentFlag.AlignCenter)
        ultrasonic_sensor_meta_info_layout.addWidget(_SensorMetaInfoWidget(SensorMeta("Ultrasonic", "Super", "0.0.0.10", "Arduino LC")), alignment=Qt.AlignmentFlag.AlignCenter)
        
        _, sonar_layout = create_widget(self.main_layout, QVBoxLayout)
        
        safety_slider = QSlider(Qt.Orientation.Horizontal)
        safety_slider.setValue(30)
        
        self.sonar_widget = SonarWidget(safety_slider.value())
        safety_slider.valueChanged.connect(self.safety_slider_moved)
        self.sonar.bluetooth.set_data_point(("angles", "distances"), lambda angles, distances: self.sonar_widget.update_sonar(angles, distances))
        
        sonar_layout.addWidget(self.sonar_widget)
        sonar_layout.addWidget(LabeledField("Safety Distance", safety_slider, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
        
        activate_cb.click()
        activate_cb.click()
    
    def safety_slider_moved(self, value: int):
        self.sonar_widget.safety_limit = value
        self.sonar.bluetooth.send_message(f"SAFETY:{self.sonar_widget.safety_limit}")
        self.sonar_widget.update_sonar(self.sonar_widget.latest_angles, self.sonar_widget.latest_distances)
    
    def toogle_activation_state(self, state):
        self.labeled_field.setDisabled(not state)
        if self.sonar.bluetooth.connected:
            self.sonar.bluetooth.send_message("SECURITY-ACTIVE" if state else "NOT-SECURITY-ACTIVE")




