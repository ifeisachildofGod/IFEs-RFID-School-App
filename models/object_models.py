from dataclasses import dataclass
from os import PathLike
from models.data_models import *

@dataclass
class Class:
    id: str
    
    level_name: str
    class_name: str
    name: str

@dataclass
class Subject:
    id: str  # Not unique
    
    name: str
    cls: Class
    periods: list[tuple[str, int]]

@dataclass
class Teacher:
    id: str
    IUD: str
    
    name: CharacterName
    department: Department
    subjects: list[Subject]
    img_path: str | PathLike
    attendance: dict[str, "AttendanceEntry"]

@dataclass
class Prefect:
    id: str
    IUD: str
    
    name: CharacterName
    post_name: str
    cls: Class
    img_path: str | PathLike
    duties: dict[str, list[str]]
    attendance: dict[str, "AttendanceEntry"]


@dataclass
class AttendanceEntry:
    time: Time
    day: str
    date: int
    month: str
    year: int
    
    staff: Teacher | Prefect | None = None


@dataclass
class Sensor:
    meta_data: SensorMeta
    img_path: str
    reading: LiveData | None = None

