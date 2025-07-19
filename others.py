
from typing import Callable
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QScrollArea, QLayout
)

from PyQt6.QtCore import QThread, pyqtSignal

DAYS_OF_THE_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS_OF_THE_YEAR = {
    "January": 31,
    "February": 29,
    "March": 31,
    "April": 30,
    "May": 31,
    "June": 30,
    "July": 31,
    "August": 31,
    "September": 30,
    "October": 31,
    "November": 30,
    "December": 31,
}


def get_attendance_time_interval(min_timeline_dates, max_timeline_dates):
    interval = None
    start_days = None
    end_days = None
    for index, (month, _) in enumerate(MONTHS_OF_THE_YEAR.items()):
        if min_timeline_dates.month == month:
            start_days = sum(list(MONTHS_OF_THE_YEAR.values())[:index]) + min_timeline_dates.date
        if max_timeline_dates.month == month:
            year_addition = (max_timeline_dates.year - min_timeline_dates.year) * 360
            end_days = sum(list(MONTHS_OF_THE_YEAR.values())[:index]) + max_timeline_dates.date + year_addition
        
        if start_days is not None and end_days is not None:
            diff = end_days - start_days
            week_amt = int(diff / 7)
            interval = week_amt, week_amt % 7
            break
    
    return interval


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

class Thread(QThread):
    crashed = pyqtSignal(Exception)
    
    def __init__(self, func: Callable):
        super().__init__()
        self.func = func
    
    def run(self):
        try:
            self.func()
        except Exception as e:
            self.crashed.emit(e)
            self.exit(-1)

