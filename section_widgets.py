
import time
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
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDrag, QDragEnterEvent, QDragMoveEvent, QDropEvent, QAction, QImage, QPixmap
from models import Prefect, Teacher, CharacterName
from theme import THEME_MANAGER


class BaseWidget(QWidget):
    def __init__(self, layout_type: type[QHBoxLayout] | type[QVBoxLayout] = QHBoxLayout):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.container = QWidget()
        
        self.main_layout = layout_type()
        self.container.setLayout(self.main_layout)
        
        layout.addWidget(self.container)
    
    def positionify(self, number: str, default: str | None = ...):
        suffix = ("st" if number.endswith("1") and number != "11" else ("nd" if number.endswith("2") and number != "12" else "rd" if number.endswith("3") and number != "13" else "th"))
        
        if not number.isnumeric():
            if not isinstance(default, ellipsis):
                suffix = (default if default is not None else "")
            else:
                raise Exception(f"Text: ({number}) is not numeric")
            
        return number + suffix
    
    def create_widget(self, parent_layout: QLayout | None, layout_type: type[QHBoxLayout] | type[QVBoxLayout] | type[QGridLayout]):
        widget = QWidget()
        layout = layout_type()
        widget.setLayout(layout)
        
        if parent_layout is not None:
            parent_layout.addWidget(widget)
        
        return widget, layout
    
    def create_scrollable_widget(self, parent_layout: QLayout | None, layout_type: type[QHBoxLayout] | type[QVBoxLayout]):
        scroll_widget = QScrollArea()
        scroll_widget.setWidgetResizable(True)
        
        widget = QWidget()
        scroll_widget.setWidget(widget)
        layout = layout_type(widget)
        
        if parent_layout is not None:
            parent_layout.addWidget(scroll_widget)
        
        return scroll_widget, layout

class CharacterNameWidget(QWidget):
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

class LabeledField(QWidget):
    def __init__(self, title: str, inner_widget: QWidget, min_size: bool = True, parent=None):
        super().__init__(parent)
        
        if min_size:
            self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        
        self.setStyleSheet("""
            #TitleLabel {
                color: gray;
                font-size: 11px;
                padding: 0 4px;
                padding-bottom: 0px;
            }
            #WrapWidget {
                border: 1px solid #aaa;
                border-radius: 6px;
            }
        """)
        
        # Title Label (floating effect)
        self.label = QLabel(title)
        self.label.setObjectName("TitleLabel")
        
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Frame to wrap the actual widget with border
        self.widget = QWidget()
        self.widget.setObjectName("WrapWidget")
        
        widget_layout = QVBoxLayout(self.widget)
        # widget_layout.setContentsMargins(5, 0, 5, 5)  # leave space for label
        widget_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignLeft)
        widget_layout.addWidget(inner_widget)
        
        # Stack label over the widget
        main_layout = QVBoxLayout(self)
        # main_layout.setContentsMargins(4, 10, 4, 4)
        main_layout.setSpacing(0)
        # main_layout.addWidget(self.label)
        main_layout.addWidget(self.widget)
        
        self.setLayout(main_layout)

    def get_widget(self):
        return self.widget.findChild(QWidget)

class TeacherWidget(BaseWidget):
    def __init__(self, teacher: Teacher):
        super().__init__()
        # self.theme = Theme()
        self.container.setProperty("class", "TeacherWidget")
        
        self.teacher = teacher
        
        _, layout_1 = self.create_widget(self.main_layout, QVBoxLayout)
        
        label = QLabel(self.container)
        pixmap = QPixmap(self.teacher.img_path)
        label.setPixmap(pixmap)
        label.setScaledContents(True)  # Optional: scale image to fit label
        
        layout_1.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        # layout_1.addStretch()
        
        widget_1_2, layout_1_2 = self.create_widget(None, QHBoxLayout)
        
        layout_1.addWidget(widget_1_2)
        
        day, month, date, t, year = time.ctime().split()
        hour, minute, sec = t.split(":")
        
        widget_1_2_1, layout_1_2_1 = self.create_widget(None, QHBoxLayout)
        
        layout_1_2_1.addWidget(LabeledField("Day", QLabel(day)))
        layout_1_2_1.addWidget(LabeledField("Date", QLabel(f"{self.positionify(date)} of {month}, {year}")))
        
        layout_1_2.addWidget(LabeledField("Day", widget_1_2_1))
        
        widget_1_2_2, layout_1_2_2 = self.create_widget(None, QHBoxLayout)
        
        layout_1_2_2.addWidget(LabeledField("Hr", QLabel(hour)))
        layout_1_2_2.addWidget(LabeledField("Min", QLabel(minute)))
        layout_1_2_2.addWidget(LabeledField("Sec", QLabel(sec)))
        
        layout_1_2.addWidget(LabeledField("Time", widget_1_2_2))
        
        _, layout_2 = self.create_widget(self.main_layout, QVBoxLayout)
        
        name_widget = CharacterNameWidget(self.teacher.name)
        layout_2.addWidget(name_widget)
        
        _, layout_2_2 = self.create_widget(layout_2, QVBoxLayout)
        
        widget_2_2_2, layout_2_2_2 = self.create_scrollable_widget(None, QVBoxLayout)
        
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
            widget_2_2_2_1, layout_2_2_2_1 = self.create_widget(None, QGridLayout)
            
            for index, ((_, cls_name), periods) in enumerate(subject_data.items()):
                widget_2_2_2_1_1, layout_2_2_2_1_1 = self.create_widget(None, QVBoxLayout)
                for period in periods:
                    layout_2_2_2_1_1.addWidget(QLabel(f"{self.positionify(str(period))} period"), alignment=Qt.AlignmentFlag.AlignTop)
                layout_2_2_2_1.addWidget(LabeledField(cls_name, widget_2_2_2_1_1), int(index / 3), index % 3)
            layout_2_2_2.addWidget(LabeledField(subject_name, widget_2_2_2_1))
    
            
            
        


class PrefectWidget(BaseWidget):
    def __init__(self, prefect: Prefect):
        super().__init__()
        # self.theme = Theme()
        self.container.setProperty("class", "PrefectWidget")
        
        self.prefect = prefect
        
        _, layout_1 = self.create_widget(self.main_layout, QVBoxLayout)
        
        label = QLabel(self.container)
        pixmap = QPixmap(self.prefect.img_path)
        label.setPixmap(pixmap)
        label.setScaledContents(True)  # Optional: scale image to fit label
        
        layout_1.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        # layout_1.addStretch()
        
        widget_1_2, layout_1_2 = self.create_widget(None, QHBoxLayout)
        
        layout_1.addWidget(widget_1_2)
        
        day, month, date, t, year = time.ctime().split()
        hour, minute, sec = t.split(":")
        
        widget_1_2_1, layout_1_2_1 = self.create_widget(None, QHBoxLayout)
        
        layout_1_2_1.addWidget(LabeledField("Day", QLabel(day)))
        layout_1_2_1.addWidget(LabeledField("Date", QLabel(f"{self.positionify(date)} of {month}, {year}")))
        
        layout_1_2.addWidget(LabeledField("Day", widget_1_2_1))
        
        widget_1_2_2, layout_1_2_2 = self.create_widget(None, QHBoxLayout)
        
        layout_1_2_2.addWidget(LabeledField("Hr", QLabel(hour)))
        layout_1_2_2.addWidget(LabeledField("Min", QLabel(minute)))
        layout_1_2_2.addWidget(LabeledField("Sec", QLabel(sec)))
        
        layout_1_2.addWidget(LabeledField("Time", widget_1_2_2))
        
        
        _, layout_2 = self.create_widget(self.main_layout, QVBoxLayout)
        
        name_widget = CharacterNameWidget(self.prefect.name)
        layout_2.addWidget(name_widget)
        
        widget_2_2, layout_2_2 = self.create_widget(None, QHBoxLayout)
        
        layout_2_2.addWidget(LabeledField("Class", QLabel(self.prefect.cls.name)))
        
        widget_1_3_1, layout_1_3_1 = self.create_scrollable_widget(None, QVBoxLayout)
        
        for index, duty in enumerate(self.prefect.duties):
            layout_1_3_1.addWidget(QLabel(f"{index + 1}. {duty}"))
        
        layout_2_2.addWidget(LabeledField("Duties", widget_1_3_1, False))
        
        layout_2.addWidget(widget_2_2)
        