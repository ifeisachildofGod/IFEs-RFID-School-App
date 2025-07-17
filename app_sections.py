
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
from models import *
from section_widgets import *


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
        
        # b = QRadioButton("Hello")
        # p = PrefectWidget(
        #     Prefect(
        #         "12010232012",
        #         CharacterName("Eze", "Emmanuel", "Udochukwu", "Emma E.U"),
        #         "Parade Commander",
        #         Class("212123321231212123113", "SS2", "D", "SS2 D"),
        #         "img.png",
        #         ["Morning", "Labour", "Cadet training"]
        #         )
        #     )
        
        # t = TeacherWidget(
        #     Teacher(
        #         "13123231323",
        #         CharacterName("Hamza", "Yunusa", "George", "Sambisa"),
        #         [
        #             Subject("23123121231212132123", "Maths", Class("212123321231212123113", "SS2", "D", "SS2 D"), [("Monday", 8), ("Monday", 9)]),
        #             Subject("23123121231252132123", "Maths", Class("212123321231212123113", "SS2", "D", "SS2 D"), [("Tuesday", 1), ("Tuesday", 2)]),
        #             Subject("23123121221212132123", "Maths", Class("212123321231212123113", "SS2", "D", "SS2 D"), [("Friday", 4), ("Friday", 5)]),
        #             Subject("23123121231212132103", "Maths", Class("212123321231212123113", "SS2", "D", "SS2 D"), [("Saturday", 8), ("Saturday", 9)]),
        #             Subject("23123121231612132123", "Maths", Class("212123321231212123113", "SS2", "D", "SS2 D"), [("Wednesday", 8), ("Wednesday", 9)]),
        #             Subject("23123121231292132123", "Maths", Class("212123321231212123113", "SS2", "D", "SS2 D"), [("Thursday", 8), ("Thursday", 9)]),
        #             ],
        #         "img.png"
        #         )
        #     )
        
        # self.main_layout.addWidget(b)
        # self.main_layout.addWidget(p)
        # self.main_layout.addWidget(t, alignment=Qt.AlignmentFlag.AlignTop)
        
        self.main_layout.addStretch()
        
        layout.addWidget(scroll_widget)

class SchoolManager(BaseListWidget):
    def __init__(self):
        super().__init__()
    
    def keyPressEvent(self, a0):
        widget = None
        
        p = Prefect(
                    "12010232012",
                    CharacterName("Eze", "Emmanuel", "Udochukwu", "Emma E.U"),
                    "Parade Commander",
                    Class("212123321231212123113", "SS2", "D", "SS2 D"),
                    "img.png",
                    ["Morning", "Labour", "Cadet training"]
                )
        if a0.key() == 16777220:
            widget = AttendanceTeacherWidget(
                    Teacher(
                        "13123231323",
                        CharacterName("Hamza", "Yunusa", "George", "Sambisa"),
                        [
                            Subject("23123121221212132123", "Maths", Class("212123321231212123113", "SS2", "D", "SS2 D"), [("Tuesday", 8), ("Monday", 9)]),
                            Subject("23123121221212132123", "Maths", Class("212123321231242123113", "SS2", "F", "SS2 F"), [("Tuesday", 1), ("Tuesday", 2)]),
                            Subject("23123121231212132103", "English", Class("2121233212312152123113", "SS3", "E", "SS3 E"), [("Tuesday", 4), ("Tuesday", 5)]),
                            Subject("23123121231212132103", "English", Class("212123323231212123113", "SS1", "B", "SS1 B"), [("Tuesday", 8), ("Tuesday", 9)]),
                            Subject("23123121231212132103", "English", Class("212123321231212123113", "SS2", "D", "SS2 D"), [("Tuesday", 8), ("Wednesday", 9)]),
                            Subject("23123121231212132103", "English", Class("212123321231217123113", "SS2", "E", "SS2 E"), [("Tuesday", 8), ("Tuesday", 9)]),
                            ],
                        "img.png"
                )
            )
        elif a0.text() == "p":
            widget = AttendancePrefectWidget(p)
        
        self.main_layout.insertWidget(len(self.main_layout.children()), widget, alignment=Qt.AlignmentFlag.AlignTop)
        return super().keyPressEvent(a0)

class EditorWidget(BaseListWidget):
    def __init__(self):
        super().__init__()
    
    def keyPressEvent(self, a0):
        p = Prefect(
                    "12010232012",
                    CharacterName("Eze", "Emmanuel", "Udochukwu", "Emma E.U"),
                    "Parade Commander",
                    Class("212123321231212123113", "SS2", "D", "SS2 D"),
                    "img.png",
                    ["Morning", "Labour", "Cadet training"]
                )
        
        if a0.key() == 16777220:
            self.main_layout.insertWidget(len(self.main_layout.children()), PrefectWidget(p), alignment=Qt.AlignmentFlag.AlignTop)
        
        return super().keyPressEvent(a0)


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


class SensorWidget(BaseWidget):
    def __init__(self, sensor: Sensor):
        super().__init__(sensor.meta_data.sensor_type)
        # self.container.setProperty("class", "GasWidget")
        
        self.sensor = sensor
        
        _, layout_1 = create_widget(self.main_layout, QVBoxLayout)
        
        label = QLabel(self.container)
        pixmap = QPixmap(self.sensor.img_path)
        label.setPixmap(pixmap)
        label.setScaledContents(True)  # Optional: scale image to fit label
        
        layout_1.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
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


