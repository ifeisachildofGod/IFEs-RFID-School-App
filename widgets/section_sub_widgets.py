
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QLabel,
    QSizePolicy, QStackedWidget
)

from PyQt6.QtCore import Qt, QPoint

from models.data_models import *
from models.object_models import *
from widgets.base_widgets import *
from widgets.extra_widgets import *
from models.collection_data_models import *


class BaseEditorWidget(QWidget):
    def __init__(self, data: AppData, base: Prefect | Teacher, parent_widget: QStackedWidget, curr_index: int, card_scanner_index: int, staff_data_index: int):
        super().__init__()
        
        self.data = data
        
        self.base = base
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.container = QWidget()
        self.main_layout = QVBoxLayout()
        self.container.setLayout(self.main_layout)
        
        layout.addWidget(self.container)
        
        self.curr_index = curr_index
        
        self.staff_data_index = staff_data_index
        self.card_scanner_index = card_scanner_index
        
        self.parent_widget = parent_widget
        
        _, main_info_layout = create_widget(self.main_layout, QHBoxLayout)
        
        image = Image(self.base.img_path, parent=self.container, height=200)
        
        main_info_layout.addWidget(image, alignment=Qt.AlignmentFlag.AlignLeft)
        main_info_layout.addStretch()
        
        name_label = QLabel(f"{self.base.name.sur} {self.base.name.first}, {self.base.name.middle}")
        
        name_label.setStyleSheet("font-size: 50px")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_info_layout.addWidget(name_label, Qt.AlignmentFlag.AlignRight)
        
        self.options_button = QPushButton("☰")
        self.options_button.setProperty("class", "options-button")
        self.options_button.setFixedSize(40, 40)
        self.options_button.clicked.connect(self.toogle_options)
        
        self.options_menu = OptionsMenu({"Set IUD": self.set_iud, "View Punctuality Data": self.view_punctuality_data})
        
        main_info_layout.addWidget(self.options_button, alignment=Qt.AlignmentFlag.AlignTop)
        
        _, self.sub_info_layout = create_widget(self.main_layout, QHBoxLayout)
        
        iud_label = QLabel(self.base.IUD if self.base.IUD is not None else "No set IUD")
        iud_label.setStyleSheet("font-weight: bold;")
        
        self.sub_info_layout.addWidget(LabeledField("IUD", iud_label), alignment=Qt.AlignmentFlag.AlignLeft)
    
    def set_iud(self):
        card_scanner_widget: CardScanScreenWidget = self.parent_widget.widget(self.card_scanner_index)
        card_scanner_widget.set_self(self.base, self.curr_index)
        
        self.parent_widget.setCurrentIndex(self.card_scanner_index)
    
    def view_punctuality_data(self):
        card_scanner_widget: StaffDataWidget = self.parent_widget.widget(self.staff_data_index)
        card_scanner_widget.set_self(self.base, self.curr_index)
        
        self.parent_widget.setCurrentIndex(self.staff_data_index)
    
    def toogle_options(self):
        if self.options_menu.isVisible():
            self.options_menu.hide()
        else:
            # Position below the options button
            button_pos = self.options_button.mapToGlobal(QPoint(-100, self.options_button.height()))
            self.options_menu.move(button_pos)
            self.options_menu.show()

class BaseAttendanceWidget(QWidget):
    def __init__(self, name: str, layout_type: type[QHBoxLayout] | type[QVBoxLayout] = QHBoxLayout):
        super().__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.container = QWidget()
        
        self.main_layout = layout_type()
        self.container.setLayout(self.main_layout)
        
        self.labeled_container = LabeledField(name, self.container)
        
        layout.addWidget(self.labeled_container)
    
    def full_name_day(self, day: str):
        return {
            "mon": "Monday",
            "tue": "Tuesday",
            "wed": "Wednesday",
            "thur": "Thursday",
            "fri": "Friday"
        }[day.lower()]
    
    def positionify(self, number: str, default: str | None = ...):
        suffix = ("st" if number.endswith("1") and number != "11" else ("nd" if number.endswith("2") and number != "12" else "rd" if number.endswith("3") and number != "13" else "th"))
        
        if not number.isnumeric():
            if not isinstance(default, ellipsis):
                suffix = (default if default is not None else "")
            else:
                raise Exception(f"Text: ({number}) is not numeric")
            
        return number + suffix


class AttendanceTeacherWidget(BaseAttendanceWidget):
    def __init__(self, data: AttendanceEntry):
        super().__init__("Teacher")
        
        self.labeled_container.setProperty("class", "AttendanceTeacherWidget")
        
        self.teacher = data.staff
        
        _, layout_1 = create_widget(self.main_layout, QVBoxLayout)
        
        image = Image(self.teacher.img_path, parent=self.container)
        
        layout_1.addWidget(image, alignment=Qt.AlignmentFlag.AlignCenter)
        # layout_1.addStretch()
        
        widget_1_2, layout_1_2 = create_widget(None, QHBoxLayout)
        
        layout_1.addWidget(widget_1_2)
        
        widget_1_2_1, layout_1_2_1 = create_widget(None, QHBoxLayout)
        
        layout_1_2_1.addWidget(LabeledField("Day", QLabel(data.day)))
        layout_1_2_1.addWidget(LabeledField("Date", QLabel(f"{self.positionify(str(data.date))} of {data.month}, {data.year}")))
        
        layout_1_2.addWidget(LabeledField("Day", widget_1_2_1))
        
        widget_1_2_2, layout_1_2_2 = create_widget(None, QHBoxLayout)
        
        layout_1_2_2.addWidget(LabeledField("Hr", QLabel(str(data.time.hour))))
        layout_1_2_2.addWidget(LabeledField("Min", QLabel(str(data.time.min))))
        layout_1_2_2.addWidget(LabeledField("Sec", QLabel(str(data.time.sec))))
        
        layout_1_2.addWidget(LabeledField("Time", widget_1_2_2))
        
        _, layout_2 = create_widget(self.main_layout, QVBoxLayout)
        
        name_widget = CharacterNameWidget(self.teacher.name)
        layout_2.addWidget(name_widget)
        
        _, layout_2_2 = create_widget(layout_2, QVBoxLayout)
        
        widget_2_2_2, layout_2_2_2 = create_scrollable_widget(None, QVBoxLayout)
        
        layout_2_2.addWidget(LabeledField("Subjects", widget_2_2_2, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        
        periods_data: dict[tuple[str, str], dict[tuple[str, str], list[int]]] = {}
        
        for subject in self.teacher.subjects:
            for day_name, period in subject.periods:
                if data.day == day_name:
                    key = subject.id, subject.name
                    sub_key = subject.cls.id, subject.cls.name
                    
                    if periods_data.get(key) is None:
                        periods_data[key] = {}
                    if periods_data[key].get(sub_key) is None:
                        periods_data[key][sub_key] = []
                    periods_data[key][sub_key].append(period)
        
        for (_, subject_name), subject_data in periods_data.items():
            widget_2_2_2_1, layout_2_2_2_1 = create_widget(None, QGridLayout)
            
            for index, ((_, cls_name), periods) in enumerate(subject_data.items()):
                widget_2_2_2_1_1, layout_2_2_2_1_1 = create_widget(None, QVBoxLayout)
                for period in periods:
                    layout_2_2_2_1_1.addWidget(QLabel(f"{self.positionify(str(period))} period"), alignment=Qt.AlignmentFlag.AlignTop)
                layout_2_2_2_1.addWidget(LabeledField(cls_name, widget_2_2_2_1_1), int(index / 3), index % 3)
            layout_2_2_2.addWidget(LabeledField(subject_name, widget_2_2_2_1))

class AttendancePrefectWidget(BaseAttendanceWidget):
    def __init__(self, data: AttendanceEntry):
        super().__init__("Prefect")
        
        self.labeled_container.setProperty("class", "AttendancePrefectWidget")
        
        self.prefect = data.staff
        
        _, layout_1 = create_widget(self.main_layout, QVBoxLayout)
        
        image = Image(self.prefect.img_path, parent=self.container)
        
        layout_1.addWidget(image, alignment=Qt.AlignmentFlag.AlignCenter)
        # layout_1.addStretch()
        
        widget_1_2, layout_1_2 = create_widget(None, QHBoxLayout)
        
        layout_1.addWidget(widget_1_2)
        
        widget_1_2_1, layout_1_2_1 = create_widget(None, QHBoxLayout)
        
        layout_1_2_1.addWidget(LabeledField("Day", QLabel(data.day)))
        layout_1_2_1.addWidget(LabeledField("Date", QLabel(f"{self.positionify(str(data.date))} of {data.month}, {data.year}")))
        
        layout_1_2.addWidget(LabeledField("Day", widget_1_2_1))
        
        widget_1_2_2, layout_1_2_2 = create_widget(None, QHBoxLayout)
        
        layout_1_2_2.addWidget(LabeledField("Hr", QLabel(str(data.time.hour))))
        layout_1_2_2.addWidget(LabeledField("Min", QLabel(str(data.time.min))))
        layout_1_2_2.addWidget(LabeledField("Sec", QLabel(str(data.time.sec))))
        
        layout_1_2.addWidget(LabeledField("Time", widget_1_2_2))
        
        _, layout_2 = create_widget(self.main_layout, QVBoxLayout)
        
        name_widget = CharacterNameWidget(self.prefect.name)
        layout_2.addWidget(name_widget)
        
        widget_2_2, layout_2_2 = create_widget(None, QHBoxLayout)
        
        layout_2_2.addWidget(LabeledField("Class", QLabel(self.prefect.cls.name)))
        
        widget_1_3_1, layout_1_3_1 = create_scrollable_widget(None, QVBoxLayout)
        
        for index, duty in enumerate(self.prefect.duties.get(data.day, [])):
            layout_1_3_1.addWidget(QLabel(f"{index + 1}. {duty}"))
        
        layout_2_2.addWidget(LabeledField("Duties", widget_1_3_1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        
        layout_2.addWidget(widget_2_2)


class EditorPrefectWidget(BaseEditorWidget):
    def __init__(self, data: AppData, prefect: Prefect, parent_widget: QStackedWidget, curr_index: int, card_scanner_index: int, staff_data_index: int):
        super().__init__(data, prefect, parent_widget, curr_index, card_scanner_index, staff_data_index)
        self.container.setProperty("class", "EditorPrefectWidget")
        
        self.sub_info_layout.addWidget(LabeledField("Post", QLabel(self.base.post_name)), alignment=Qt.AlignmentFlag.AlignCenter)
        self.sub_info_layout.addWidget(LabeledField("Class", QLabel(self.base.cls.name)), alignment=Qt.AlignmentFlag.AlignRight)

class EditorTeacherWidget(BaseEditorWidget):
    def __init__(self, data: AppData, teacher: Teacher, parent_widget: QStackedWidget, curr_index: int, card_scanner_index: int, staff_data_index: int):
        super().__init__(data, teacher, parent_widget, curr_index, card_scanner_index, staff_data_index)
        self.container.setProperty("class", "EditorTeacherWidget")
        
        self.sub_info_layout.addWidget(LabeledField("Dept", QLabel(self.base.department.name), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum), alignment=Qt.AlignmentFlag.AlignRight)


