
import time
import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QApplication, QGridLayout,
    QLineEdit, QPushButton, QScrollArea,
    QTableWidget, QLabel, QFrame,
    QAbstractItemView, QHeaderView, QMenu, QSizePolicy,
    QProgressBar, QCheckBox, QMainWindow,
    QStackedWidget, QMessageBox, QFileDialog, QToolBar,
    QRadioButton, QLayout
)
from PyQt6.QtCore import Qt, QPoint
from matplotlib.figure import Figure
from models import *
from base_widgets import *
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtGui import QDrag, QDragEnterEvent, QDragMoveEvent, QDropEvent, QAction, QImage, QPixmap

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


class BaseWidget(QWidget):
    def __init__(self, name: str, layout_type: type[QHBoxLayout] | type[QVBoxLayout] = QHBoxLayout):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.container = QWidget()
        
        self.main_layout = layout_type()
        self.container.setLayout(self.main_layout)
        
        container = LabeledField(name, self.container)
        container.setProperty("class", name)
        
        layout.addWidget(container)
    
    def positionify(self, number: str, default: str | None = ...):
        suffix = ("st" if number.endswith("1") and number != "11" else ("nd" if number.endswith("2") and number != "12" else "rd" if number.endswith("3") and number != "13" else "th"))
        
        if not number.isnumeric():
            if not isinstance(default, ellipsis):
                suffix = (default if default is not None else "")
            else:
                raise Exception(f"Text: ({number}) is not numeric")
            
        return number + suffix


class _CharacterNameWidget(QWidget):
    def __init__(self, name: CharacterName):
        super().__init__()
        self.name = name
        
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        widget_2_1 = QWidget()
        layout_2_1 = QVBoxLayout()
        widget_2_1.setLayout(layout_2_1)
        
        widget_2_1_1 = QWidget()
        layout_2_1_1 = QHBoxLayout()
        widget_2_1_1.setLayout(layout_2_1_1)
        layout_2_1.addWidget(widget_2_1_1)
        
        name_1 = LabeledField("Surname", QLabel(self.name.sur))
        name_2 = LabeledField("First name", QLabel(self.name.first))
        name_3 = LabeledField("Middle name", QLabel(self.name.middle))
        
        layout_2_1_1.addWidget(name_1)
        layout_2_1_1.addWidget(name_2)
        layout_2_1_1.addWidget(name_3)
        
        widget_2_1_2 = QWidget()
        layout_2_1_2 = QHBoxLayout()
        widget_2_1_2.setLayout(layout_2_1_2)
        layout_2_1.addWidget(widget_2_1_2)
        
        name_4 = LabeledField("Other name", QLabel(self.name.other if self.name.other is not None else "No other name"))
        name_5 = LabeledField("Abbreviation", QLabel(self.name.abrev))
        
        layout_2_1_2.addWidget(name_4)
        layout_2_1_2.addWidget(name_5, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.main_layout.addWidget(LabeledField("Names", widget_2_1))

class AttendanceTeacherWidget(BaseWidget):
    def __init__(self, teacher: Teacher):
        super().__init__("Teacher")
        
        self.teacher = teacher
        
        _, layout_1 = create_widget(self.main_layout, QVBoxLayout)
        
        label = QLabel(self.container)
        pixmap = QPixmap(self.teacher.img_path)
        label.setPixmap(pixmap)
        label.setScaledContents(True)  # Optional: scale image to fit label
        
        layout_1.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        # layout_1.addStretch()
        
        widget_1_2, layout_1_2 = create_widget(None, QHBoxLayout)
        
        layout_1.addWidget(widget_1_2)
        
        day, month, date, t, year = time.ctime().split()
        hour, minute, sec = t.split(":")
        
        widget_1_2_1, layout_1_2_1 = create_widget(None, QHBoxLayout)
        
        layout_1_2_1.addWidget(LabeledField("Day", QLabel(day)))
        layout_1_2_1.addWidget(LabeledField("Date", QLabel(f"{self.positionify(date)} of {month}, {year}")))
        
        layout_1_2.addWidget(LabeledField("Day", widget_1_2_1))
        
        widget_1_2_2, layout_1_2_2 = create_widget(None, QHBoxLayout)
        
        layout_1_2_2.addWidget(LabeledField("Hr", QLabel(hour)))
        layout_1_2_2.addWidget(LabeledField("Min", QLabel(minute)))
        layout_1_2_2.addWidget(LabeledField("Sec", QLabel(sec)))
        
        layout_1_2.addWidget(LabeledField("Time", widget_1_2_2))
        
        _, layout_2 = create_widget(self.main_layout, QVBoxLayout)
        
        name_widget = _CharacterNameWidget(self.teacher.name)
        layout_2.addWidget(name_widget)
        
        _, layout_2_2 = create_widget(layout_2, QVBoxLayout)
        
        widget_2_2_2, layout_2_2_2 = create_scrollable_widget(None, QVBoxLayout)
        
        layout_2_2.addWidget(LabeledField("Subjects", widget_2_2_2, False))
        
        periods_data = {}
        
        for subject in self.teacher.subjects:
            for day_name, period in subject.periods:
                if day in day_name:
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

class AttendancePrefectWidget(BaseWidget):
    def __init__(self, prefect: Prefect):
        super().__init__("Prefect")
        self.container.setProperty("class", "PrefectWidget")
        
        self.prefect = prefect
        
        _, layout_1 = create_widget(self.main_layout, QVBoxLayout)
        
        label = QLabel(self.container)
        pixmap = QPixmap(self.prefect.img_path)
        label.setPixmap(pixmap)
        label.setScaledContents(True)  # Optional: scale image to fit label
        
        layout_1.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        # layout_1.addStretch()
        
        widget_1_2, layout_1_2 = create_widget(None, QHBoxLayout)
        
        layout_1.addWidget(widget_1_2)
        
        day, month, date, t, year = time.ctime().split()
        hour, minute, sec = t.split(":")
        
        widget_1_2_1, layout_1_2_1 = create_widget(None, QHBoxLayout)
        
        layout_1_2_1.addWidget(LabeledField("Day", QLabel(day)))
        layout_1_2_1.addWidget(LabeledField("Date", QLabel(f"{self.positionify(date)} of {month}, {year}")))
        
        layout_1_2.addWidget(LabeledField("Day", widget_1_2_1))
        
        widget_1_2_2, layout_1_2_2 = create_widget(None, QHBoxLayout)
        
        layout_1_2_2.addWidget(LabeledField("Hr", QLabel(hour)))
        layout_1_2_2.addWidget(LabeledField("Min", QLabel(minute)))
        layout_1_2_2.addWidget(LabeledField("Sec", QLabel(sec)))
        
        layout_1_2.addWidget(LabeledField("Time", widget_1_2_2))
        
        _, layout_2 = create_widget(self.main_layout, QVBoxLayout)
        
        name_widget = _CharacterNameWidget(self.prefect.name)
        layout_2.addWidget(name_widget)
        
        widget_2_2, layout_2_2 = create_widget(None, QHBoxLayout)
        
        layout_2_2.addWidget(LabeledField("Class", QLabel(self.prefect.cls.name)))
        
        widget_1_3_1, layout_1_3_1 = create_scrollable_widget(None, QVBoxLayout)
        
        for index, duty in enumerate(self.prefect.duties):
            layout_1_3_1.addWidget(QLabel(f"{index + 1}. {duty}"))
        
        layout_2_2.addWidget(LabeledField("Duties", widget_1_3_1, False))
        
        layout_2.addWidget(widget_2_2)

class PrefectWidget(QWidget):
    def __init__(self, prefect: Prefect):
        super().__init__()
        
        self.prefect = prefect
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.container = QWidget()
        self.main_layout = QVBoxLayout()
        self.container.setLayout(self.main_layout)
        
        layout.addWidget(self.container)
        
        _, main_info_layout = create_widget(self.main_layout, QHBoxLayout)
        
        image_height = 200
        
        label = QLabel(self.container)
        pixmap = QPixmap(self.prefect.img_path)
        label.setFixedHeight(image_height)
        label.setFixedWidth(int(image_height * pixmap.size().width() / pixmap.size().height()))
        label.setScaledContents(True)  # Optional: scale image to fit label
        scaled_pixmap = pixmap.scaled(
            label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        label.setPixmap(scaled_pixmap)
        main_info_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignLeft)
        main_info_layout.addStretch()
        
        name_label = QLabel(f"{self.prefect.name.sur} {self.prefect.name.first}, {self.prefect.name.middle}")
        name_label.setStyleSheet("font-size: 50px")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_info_layout.addWidget(name_label, Qt.AlignmentFlag.AlignRight)
        
        self.option_button_size = 30
        
        self.option_button = QPushButton("")
        self.option_button.setStyleSheet(f"""
            font-size: {self.option_button_size}px;
            border-radius: {self.option_button_size / 2}px;
        """)
        self.option_button.setFixedSize(self.option_button_size, self.option_button_size)
        # self.option_button.clicked.connect(self.show_context_menu)
        self.option_button.mousePressEvent = self.show_context_menu
        
        main_info_layout.addWidget(self.option_button, alignment=Qt.AlignmentFlag.AlignTop)
        
        _, sub_info_layout = create_widget(self.main_layout, QHBoxLayout)
        
        id_label = QLabel(self.prefect.id)
        id_label.setStyleSheet("font-weight: bold;")
        
        sub_info_layout.addWidget(LabeledField("IUD", id_label), alignment=Qt.AlignmentFlag.AlignLeft)
        sub_info_layout.addWidget(LabeledField("Post", QLabel(self.prefect.post_name)), alignment=Qt.AlignmentFlag.AlignCenter)
        sub_info_layout.addWidget(LabeledField("Class", QLabel(self.prefect.cls.name)), alignment=Qt.AlignmentFlag.AlignRight)
    
    def mousePressEvent(self, a0):
        print("a", self.mapToGlobal(a0.pos()))
        return super().mousePressEvent(a0)
    
    def show_context_menu(self, a0):
        menu = QMenu(self)
        
        IUD_action = menu.addAction("Set IUD")
        puncuality_graph = menu.addAction("View punctuality graph")
        
        pos = self.mapToGlobal(self.mapTo(self.parent(), self.pos()))
        
        action = menu.exec(pos)
        
        if action == IUD_action:
            pass

