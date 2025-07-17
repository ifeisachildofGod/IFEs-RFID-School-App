from PyQt6.QtCore import pyqtSignal, pyqtBoundSignal
from dataclasses import dataclass
from os import PathLike
from typing import Callable
from models.object_models import *

@dataclass
class Time:
    sec: float
    min: int
    hour: int

@dataclass
class AttendanceData:
    attendance: dict[str, tuple[str, str, int, Time, str]]
    staff: Teacher | Prefect

@dataclass
class AppData:
    teacher_cit: Time
    prefect_cit: Time
    
    teachers: list[Teacher]
    prefects: list[Prefect]
    
    attendance_data: list[AttendanceData]

