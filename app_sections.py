
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
from PyQt6.QtCore import Qt
from models import CharacterName, Class, Prefect, PrefectDuty, Subject, Teacher
from section_widgets import PrefectWidget, TeacherWidget


class SchoolManager(QWidget):
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
        #         PrefectDuty(True, False)
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
    
    def keyPressEvent(self, a0):
        if a0.key() == 16777220:
            widget = TeacherWidget(
                    Teacher(
                        "13123231323",
                        CharacterName("Hamza", "Yunusa", "George", "Sambisa"),
                        [
                            Subject("23123121221212132123", "Maths", Class("212123321231212123113", "SS2", "D", "SS2 D"), [("Saturday", 8), ("Monday", 9)]),
                            Subject("23123121221212132123", "Maths", Class("212123321231242123113", "SS2", "F", "SS2 F"), [("Saturday", 1), ("Tuesday", 2)]),
                            Subject("23123121231212132103", "English", Class("2121233212312152123113", "SS3", "E", "SS3 E"), [("Saturday", 4), ("Saturday", 5)]),
                            Subject("23123121231212132103", "English", Class("212123323231212123113", "SS1", "B", "SS1 B"), [("Saturday", 8), ("Saturday", 9)]),
                            Subject("23123121231212132103", "English", Class("212123321231212123113", "SS2", "D", "SS2 D"), [("Saturday", 8), ("Wednesday", 9)]),
                            Subject("23123121231212132103", "English", Class("212123321231217123113", "SS2", "E", "SS2 E"), [("Saturday", 8), ("Saturday", 9)]),
                            ],
                        "img.png"
                )
            )
            widget.setProperty("class", "TeacherWidget")
            self.main_layout.insertWidget(
                len(self.main_layout.children()) - 1, widget, alignment=Qt.AlignmentFlag.AlignTop)
        return super().keyPressEvent(a0)
        
        
        