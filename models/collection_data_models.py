
from dataclasses import dataclass
from models.object_models import *


@dataclass
class AppData:
    teacher_cit: Time
    prefect_cit: Time
    
    teacher_timeline_dates: tuple[AttendanceEntry, AttendanceEntry]
    prefect_timeline_dates: tuple[AttendanceEntry, AttendanceEntry]

    attendance_data: list[AttendanceEntry]
    
    teachers: dict[str, Teacher]
    prefects: dict[str, Prefect]

