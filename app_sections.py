
from copy import deepcopy
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
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDrag, QDragEnterEvent, QDragMoveEvent, QDropEvent, QAction, QImage, QPixmap
from models.data_models import *
from models.collection_data_models import *
from section_widgets import *
from base_widgets import *
from theme import THEME_MANAGER
from matplotlib.colors import get_named_colors_mapping


DAYS_OF_THE_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

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
    def __init__(self, data: AppData):
        super().__init__()
        
        _, cit_layout = create_widget(self.main_layout, QHBoxLayout)
        
        cit_layout.addWidget(LabeledField("Teacher Check-in Time", f"{data.teacher_cit.hour} : {data.teacher_cit.min} : {data.teacher_cit.sec}", QSizePolicy.Policy.Minimum))
        cit_layout.addWidget(LabeledField("Prefect Check-in Time", f"{data.prefect_cit.hour} : {data.prefect_cit.min} : {data.prefect_cit.sec}", QSizePolicy.Policy.Minimum))
        
        _, attendance_layout = create_widget(self.main_layout, QVBoxLayout)
        
        for staff in data.attendance_data:
            if isinstance(staff, Teacher):
                widget = AttendanceTeacherWidget(staff)
            elif isinstance(staff, Prefect):
                widget = AttendancePrefectWidget(staff)
            else:
                raise TypeError(f"Type: {type(staff)} is not appropriate in AppData.attendance_data")
            
            attendance_layout.addWidget(widget)
        
        self.main_layout.addStretch()
    
    # def keyPressEvent(self, a0):
    #     widget = None
        
    #     if a0.key() == 16777220:
    #         widget = AttendanceTeacherWidget(
    #             Teacher(
    #                 "13123231323",
    #                 CharacterName("Hamza", "Yunusa", "George", "Sambisa"),
    #                 Department("department_id 1", "Humanities"),
    #                 [
    #                     Subject("23123121221212132123", "Maths", Class("212123321231212123113", "SS2", "D", "SS2 D"), [("Tuesday", 8), ("Monday", 9)]),
    #                     Subject("23123121221212132123", "Maths", Class("212123321231242123113", "SS2", "F", "SS2 F"), [("Tuesday", 1), ("Tuesday", 2)]),
    #                     Subject("23123121231212132103", "English", Class("2121233212312152123113", "SS3", "E", "SS3 E"), [("Tuesday", 4), ("Tuesday", 5)]),
    #                     Subject("23123121231212132103", "English", Class("212123323231212123113", "SS1", "B", "SS1 B"), [("Tuesday", 8), ("Tuesday", 9)]),
    #                     Subject("23123121231212132103", "English", Class("212123321231212123113", "SS2", "D", "SS2 D"), [("Tuesday", 8), ("Wednesday", 9)]),
    #                     Subject("23123121231212132103", "English", Class("212123321231217123113", "SS2", "E", "SS2 E"), [("Tuesday", 8), ("Tuesday", 9)]),
    #                     ],
    #                 "img.png"
    #             )
    #         )
    #     elif a0.text() == "p":
    #         widget = AttendancePrefectWidget(
    #             Prefect(
    #                 "12010232012",
    #                 CharacterName("Eze", "Emmanuel", "Udochukwu", "Emma E.U"),
    #                 "Parade Commander",
    #                 Class("212123321231212123113", "SS2", "D", "SS2 D"),
    #                 "img.png",
    #                 ["Morning", "Labour", "Cadet training"]
    #             )
    #         )
        
    #     self.main_layout.insertWidget(len(self.main_layout.children()), widget, alignment=Qt.AlignmentFlag.AlignTop)
    #     return super().keyPressEvent(a0)

class PrefectEditorWidget(BaseListWidget):
    def __init__(self, data: AppData):
        super().__init__()
        
        for prefect in data.prefects:
            self.main_layout.addWidget(AttendancePrefectWidget(prefect))
        
        self.main_layout.addStretch()
    
    # def keyPressEvent(self, a0):
    #     p = Prefect(
    #                 "12010232012",
    #                 CharacterName("Eze", "Emmanuel", "Udochukwu", "Emma E.U"),
    #                 "Parade Commander",
    #                 Class("212123321231212123113", "SS2", "D", "SS2 D"),
    #                 "img.png",
    #                 ["Morning", "Labour", "Cadet training"]
    #             )
        
    #     if a0.key() == 16777220:
    #         self.main_layout.insertWidget(len(self.main_layout.children()), EditorPrefectWidget(p), alignment=Qt.AlignmentFlag.AlignTop)
        
    #     return super().keyPressEvent(a0)

class TeacherEditorWidget(BaseListWidget):
    def __init__(self, data: AppData):
        super().__init__()
        
        for teacher in data.teachers:
            self.main_layout.addWidget(AttendancePrefectWidget(teacher))
        
        self.main_layout.addStretch()
    
    # def keyPressEvent(self, a0):
    #     t = Teacher(
    #             "13123231323",
    #             CharacterName("Hamza", "Yunusa", "George", "Sambisa"),
    #             Department("department_id 1", "Humanities"),
    #             [
    #                 Subject("23123121221212132123", "Maths", Class("212123321231212123113", "SS2", "D", "SS2 D"), [("Tuesday", 8), ("Monday", 9)]),
    #                 Subject("23123121221212132123", "Maths", Class("212123321231242123113", "SS2", "F", "SS2 F"), [("Tuesday", 1), ("Tuesday", 2)]),
    #                 Subject("23123121231212132103", "English", Class("2121233212312152123113", "SS3", "E", "SS3 E"), [("Tuesday", 4), ("Tuesday", 5)]),
    #                 Subject("23123121231212132103", "English", Class("212123323231212123113", "SS1", "B", "SS1 B"), [("Tuesday", 8), ("Tuesday", 9)]),
    #                 Subject("23123121231212132103", "English", Class("212123321231212123113", "SS2", "D", "SS2 D"), [("Tuesday", 8), ("Wednesday", 9)]),
    #                 Subject("23123121231212132103", "English", Class("212123321231217123113", "SS2", "E", "SS2 E"), [("Tuesday", 8), ("Tuesday", 9)]),
    #                 ],
    #             "img.png"
    #         )
        
    #     if a0.key() == 16777220:
    #         self.main_layout.insertWidget(len(self.main_layout.children()), EditorTeacherWidget(t), alignment=Qt.AlignmentFlag.AlignTop)
        
    #     return super().keyPressEvent(a0)

class AttendanceBarWidget(BaseListWidget):
    def __init__(self, data: AppData):
        super().__init__()
        
        prefects_data = []
        
        for staff_attendance_data in data.attendance_data:
            if isinstance(staff_attendance_data.staff, Prefect):
                weeks: list[list[Time]] = []
                week = []
                prev_day = "Monday"
                prev_dt = 1
                for index, (_, (day, _, dt, t, _)) in enumerate(staff_attendance_data.attendance.items()):
                    week.append(t)
                    
                    if DAYS_OF_THE_WEEK.index(day) > DAYS_OF_THE_WEEK.index(prev_day) or (prev_dt != dt and DAYS_OF_THE_WEEK.index(day) == DAYS_OF_THE_WEEK.index(prev_day)) or index + 1 == len(staff_attendance_data.attendance):
                        weeks.append(deepcopy(week))
                        week = []
                    
                    prev_day = day
                    prev_dt = dt
                
                yearly_punctuality = 0
                
                for week_time in weeks:
                    weekly_punctuality = sum([(data.prefect_cit.hour - t.hour) * 60 + (data.prefect_cit.min - t.min) * 60 + (data.prefect_cit.sec - t.sec) / 60 for t in week_time])
                    yearly_punctuality += weekly_punctuality
                    
                prefects_data.append(yearly_punctuality)
        
        sub_data = ["Emma", "Bambi", "Mikalele", "Jesse", "Tumbum"], [80, 90, 98, 79, 86]
        
        prefect_info_widget = BarWidget("Cummulative Prefect Attendance", "Prefect Names", "Yearly Attendance (%)")
        prefect_info_widget.add_data("Prefects", THEME_MANAGER.get_current_palette()["prefect"], sub_data)
        
        teacher_data = {
            "department_id 1": ("Humanities", sub_data),
            "department_id 2": ("Technology", sub_data),
            "department_id 3": ("Mathematics", sub_data),
            "department_id 4": ("English", sub_data),
            "department_id 5": ("Physics", sub_data),
        }
        
        dtd_widget, dtd_layout = create_widget(None, QVBoxLayout)
        # dtd_widget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        
        for index, (_, (name, data)) in enumerate(teacher_data.items()):
            widget = BarWidget(f"Cummulative {name} Attendance", f"{name} Department Teachers", "Yearly Attendance (%)")
            widget.add_data(name, list(get_named_colors_mapping().values())[index], data)
            
            dtd_layout.addWidget(widget)
        
        self.main_layout.addWidget(prefect_info_widget)
        self.main_layout.addWidget(LabeledField("Departmental Attendance", dtd_widget, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))

class PunctualityGraphWidget(BaseListWidget):
    def __init__(self, data: AppData):
        super().__init__()
        
        self.data = data
        
        teacher_data = {}
        prefects_data = {}
        
        for staff_attendance_data in self.data.attendance_data:
            if isinstance(staff_attendance_data.staff, Prefect):
                prefects_data[staff_attendance_data.staff.id] = self.get_punctuality_data(staff_attendance_data)
            elif isinstance(staff_attendance_data.staff, Teacher):
                teacher_data[staff_attendance_data.staff.department.id][1][staff_attendance_data.staff.id] = self.get_punctuality_data(staff_attendance_data)
        
        # sub_data = {
        #     "prefect_id 1": ("Emma", [0, 0, 0, 1, 1, 2, 2, -1, -1, -3, 0, -2, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3]),
        #     "prefect_id 2": ("Bambi", [0, 0, 0, -2, 1, 2, 2, 0, -1, -3, 0, -2, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3]),
        #     "prefect_id 3": ("Mikalele", [0, 0, -1, 0, 1, 1, 2, 0, -1, -3, 0, -2, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3]),
        #     "prefect_id 4": ("Jesse", [0, 0, 0, 1, 1, 2, 3, 0, -1, -3, 0, -2, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3]),
        #     "prefect_id 5": ("Tumbum", [0, 0, 0, 3, 1, 2, 0, 0, -1, -3, 0, -2, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3]),
        # }
        prefect_info_widget = GraphWidget("Prefects Punctuality Graph", "Time Interval (Weeks)", "Punctuality (Hours)")
        
        for index, (_, (name, data)) in enumerate(prefects_data.items()):
            prefect_info_widget.plot([i + 1 for i in range(len(data))], data, label=name, marker='o', color=list(get_named_colors_mapping().values())[index])
        
        # teacher_data = {
        #     "department_id 1": ("Humanities", sub_data),
        #     "department_id 2": ("Technology", sub_data),
        #     "department_id 3": ("Mathematics", sub_data),
        #     "department_id 4": ("English", sub_data),
        #     "department_id 5": ("Physics", sub_data),
        # }
        
        dtd_widget, dtd_layout = create_widget(None, QVBoxLayout)
        
        for _, (dep_name, dep_data) in teacher_data.items():
            dep_info_widget = GraphWidget(f"{dep_name} Department Punctuality Graph", "Time Interval (Weeks)", "Punctuality (Hours)")
            
            for index, (_, (name, info)) in enumerate(dep_data.items()):
                dep_info_widget.plot([i + 1 for i in range(len(info))], info, label=name, marker='o', color=list(get_named_colors_mapping().values())[index])
            
            dtd_layout.addWidget(dep_info_widget)
        
        self.main_layout.addWidget(prefect_info_widget)
        self.main_layout.addWidget(LabeledField("Departmental Attendance", dtd_widget, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
    
    def get_punctuality_data(self, staff_attendance_data: AttendanceData):
        prefects_plot_data: list[float] = []
        
        weeks: list[list[Time]] = []
        week = []
        prev_day = "Monday"
        prev_dt = 1
        for index, (_, (day, _, dt, t, _)) in enumerate(staff_attendance_data.attendance.items()):
            week.append(t)
            
            if DAYS_OF_THE_WEEK.index(day) > DAYS_OF_THE_WEEK.index(prev_day) or (prev_dt != dt and DAYS_OF_THE_WEEK.index(day) == DAYS_OF_THE_WEEK.index(prev_day)) or index + 1 == len(staff_attendance_data.attendance):
                weeks.append(deepcopy(week))
                week = []
            
            prev_day = day
            prev_dt = dt
        
        for week_time in weeks:
            weekly_punctuality = sum([(self.data.prefect_cit.hour - t.hour) * 60 + (self.data.prefect_cit.min - t.min) * 60 + (self.data.prefect_cit.sec - t.sec) / 60 for t in week_time])
            prefects_plot_data.append(weekly_punctuality)
        
        return staff_attendance_data.staff.name, prefects_plot_data


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
        
        self.main_layout.addWidget(LabeledField("Meta Info", widget_2_1))

class SensorWidget(QWidget):
    def __init__(self, sensor: Sensor):
        super().__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.container = QWidget()
        
        self.main_layout = QHBoxLayout()
        self.container.setLayout(self.main_layout)
        
        self.labeled_container = LabeledField(sensor.meta_data.sensor_type, self.container)
        
        layout.addWidget(self.labeled_container)
        
        self.sensor = sensor
        
        _, layout_1 = create_widget(self.main_layout, QVBoxLayout)
        
        image = Image(self.sensor.img_path, parent=self.container)
        layout_1.addWidget(image, alignment=Qt.AlignmentFlag.AlignCenter)
        # layout_1.addStretch()
        
        widget_1_2, layout_1_2 = create_widget(None, QHBoxLayout)
        
        self.reading_label = QLabel(self.sensor.reading.data_func() if self.sensor.reading is not None else "None")
        if self.sensor.reading is not None:
            self.sensor.reading.data_signal.connect(lambda data: self.reading_label.setText(str(data)))
        
        layout_1_2.addWidget(LabeledField("Reading", self.reading_label))
        
        layout_1.addWidget(widget_1_2)
        
        _, layout_2 = create_widget(self.main_layout, QVBoxLayout)
        
        meta_info_widget = _SensorMetaInfoWidget(self.sensor.meta_data)
        layout_2.addWidget(meta_info_widget)

class UltrasonicSonarWidget(QWidget):
    def __init__(self, sensor: Sensor):
        super().__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.container = QWidget()
        
        self.main_layout = QHBoxLayout()
        self.container.setLayout(self.main_layout)
        
        self.labeled_container = LabeledField(sensor.meta_data.sensor_type, self.container)
        
        layout.addWidget(self.labeled_container)
        
        sonar_widget = SonarWidget(30)
        
        ultrasonic_sensor_meta_info_widget, ultrasonic_sensor_meta_info_layout = create_widget(self.main_layout, QHBoxLayout)
        
        ultrasonic_sensor_meta_info_layout.addWidget(Image(sensor.img_path, ultrasonic_sensor_meta_info_widget))
        ultrasonic_sensor_meta_info_layout.addWidget(_SensorMetaInfoWidget(SensorMeta("Ultrasonic", "Super", "0.0.0.10", "Arduino LC")))
        
        self.main_layout.addWidget(sonar_widget)
        
        if sensor.reading is not None:
            sensor.reading.data_signal.connect(lambda angles, distances: sonar_widget.update_sonar(angles, distances))


