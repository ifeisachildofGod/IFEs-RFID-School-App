
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QLabel, QStackedWidget
)

from PyQt6.QtCore import Qt
from matplotlib.colors import get_named_colors_mapping

from models.data_models import *
from models.object_models import *
from widgets.base_widgets import *
from matplotlib.cbook import flatten
from models.collection_data_models import *


class BaseExtraWidget(QWidget):
    def __init__(self, parent_widget: QStackedWidget):
        super().__init__()
        
        layout = QVBoxLayout(self)
        
        self.container = QWidget()
        self.main_layout = QVBoxLayout()
        self.container.setLayout(self.main_layout)
        
        layout.addWidget(self.container)
        
        self.parent_widget = parent_widget
        
        _, upper_layout = create_widget(self.main_layout, QHBoxLayout)
        
        cancel_button = QPushButton("×")
        cancel_button.setFixedSize(30, 30)
        cancel_button.setStyleSheet("font-size: 25px; border-radius: 15px; background-color: #00000000;")
        cancel_button.clicked.connect(self.finished)
        
        upper_layout.addStretch()
        upper_layout.addWidget(cancel_button, Qt.AlignmentFlag.AlignRight)
        
        self.staff: Teacher | Prefect | None = None
        self.staff_index: int | None = None
    
    def set_self(self, staff: Teacher | Prefect, staff_index: int):
        self.staff = staff
        self.staff_index = staff_index
    
    def finished(self):
        self.parent_widget.setCurrentIndex(self.staff_index)
        
        self.staff = None
        self.staff_index = None


class StaffDataWidget(BaseExtraWidget):
    def __init__(self, data: AppData, parent_widget: QStackedWidget):
        super().__init__(parent_widget)
        
        self.data = data
        
        self.attendance_widget: BarWidget | None = None
        self.punctuality_widget: GraphWidget | None = None
    
    def set_self(self, staff, staff_index):
        super().set_self(staff, staff_index)
        
        if self.attendance_widget is not None:
            self.main_layout.removeWidget(self.attendance_widget)
            self.attendance_widget.deleteLater()
        
        if self.punctuality_widget is not None:
            self.main_layout.removeWidget(self.punctuality_widget)
            self.punctuality_widget.deleteLater()
        
        if isinstance(staff, Teacher):
            bar_title = f"{staff.name} Monthly Cummulative Attendance Chart"
            graph_title = f"{staff.name} Monthly Cummulative Punctuality Graph"
            week_days = list(set(flatten([[day for day, _ in s.periods] for s in staff.subjects])))
            timeline_dates = self.data.teacher_timeline_dates
        elif isinstance(staff, Prefect):
            bar_title = f"{staff.name} ({staff.post_name}) Monthly Cummulative Attendance Chart"
            graph_title = f"{staff.name} ({staff.post_name}) Monthly Average Punctuality Graph"
            week_days = list(staff.duties.keys())
            timeline_dates = self.data.prefect_timeline_dates
        
        months = []
        percentile_values = []
        
        self.attendance_widget = BarWidget(bar_title, "Time (Months)", "Attendace (%)")
        self.attendance_widget.bar_canvas.axes.set_ylim(0, 100)
        
        if staff.attendance:
            monthly_attendance_data = {}
            for attendance in staff.attendance.values():
                monthly_attendance_data[f"{attendance.month} {attendance.year}"] = monthly_attendance_data.get(f"{attendance.month} {attendance.year}", 0) + 1
            
            for date, monthly_attendance in monthly_attendance_data.items():
                month_end = AttendanceEntry(**timeline_dates[1])
                month_end.date = MONTHS_OF_THE_YEAR[timeline_dates[0].day]
                month_end.year = timeline_dates[0].year
                month_end.day = DAYS_OF_THE_WEEK[DAYS_OF_THE_WEEK.index(timeline_dates[0].day) + ((month_end.date - timeline_dates[0].date) % 7)]
                start_week_amt, rem_days = get_attendance_time_interval(timeline_dates[0], month_end)
                monthly_dta = (start_week_amt * len(week_days)) + len([d for d in week_days if d in rem_days])
                
                months.append(date)
                percentile_values.append(monthly_attendance * 100 / monthly_dta)
            
            self.attendance_widget.add_data(f"{staff.name} Attendance Data", "red", (months, percentile_values))
        
        self.main_layout.addWidget(self.attendance_widget)
        
        self.punctuality_widget = GraphWidget(graph_title, "Time", "Punctuality (Minutes)")
        
        if staff.attendance:
            prev_date = f"{list(staff.attendance.values())[0].month} {list(staff.attendance.values())[0].year}"
            
            date_months_mapping: dict[str, list[tuple[int, Time]]] = {}
            for _, attendance in staff.attendance.items():
                date = f"{attendance.month} {attendance.year}"
                
                if date != prev_date:
                    date_months_mapping[date] = [(attendance.date, attendance.time)]
                else:
                    date_months_mapping[date].append((attendance.date, attendance.time))
                
                prev_date = date
            
            plot_data: list[tuple[str, list[float]]] = []
            for date, month_time in date_months_mapping.items():
                x_data = [date for date, _ in month_time]
                months_data = [(((self.data.prefect_cit.hour - t.hour) * 60) + (self.data.prefect_cit.min - t.min) + ((self.data.prefect_cit.hour - t.hour) / 60)) for _, t in month_time]
                plot_data.append((date, x_data, months_data))
            
            for index, (date, x, y) in enumerate(plot_data):
                self.punctuality_widget.plot(x, y, label=date, marker='o', color=list(get_named_colors_mapping().values())[index])
        
        self.main_layout.addWidget(self.punctuality_widget)

class CardScanScreenWidget(BaseExtraWidget):
    def __init__(self, rfid_live_data: LiveData, parent_widget: QStackedWidget):
        super().__init__(parent_widget)
        
        self.setStyleSheet("""
            QWidget {
                background-color: darkgrey;
            }
            QLabel {
                color: white;
            }
        """)
        
        self.main_layout.addWidget(Image("img.png"), Qt.AlignmentFlag.AlignCenter)
        
        info = QLabel("Please scan RFID card")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(info, Qt.AlignmentFlag.AlignCenter)
        
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.info_label, Qt.AlignmentFlag.AlignCenter)
        
        rfid_live_data.data_signal.connect(self.scanned)
    
    def set_self(self, staff, staff_index):
        super().set_self(staff, staff_index)
        
        self.info_label.setText(f"To link an IUD to {self.staff.name} (ID: {self.staff.id})")
    
    def scanned(self, data: dict):
        self.staff.IUD = data["IUD"]
        
        self.finished()

