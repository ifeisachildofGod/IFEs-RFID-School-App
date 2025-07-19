
from os import PathLike
from communication import Bluetooth
from models.data_models import *
from dataclasses import dataclass

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
    IUD: str | None
    
    name: CharacterName
    department: Department
    subjects: list[Subject]
    img_path: str | PathLike
    attendance: list["AttendanceEntry"]

@dataclass
class Prefect:
    id: str
    IUD: str | None
    
    name: CharacterName
    post_name: str
    cls: Class
    img_path: str | PathLike
    duties: dict[str, list[str]]
    attendance: list["AttendanceEntry"]


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
    bluetooth: Bluetooth

