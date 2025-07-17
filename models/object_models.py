from PyQt6.QtCore import pyqtSignal, pyqtBoundSignal
from dataclasses import dataclass
from os import PathLike
from typing import Callable
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
    
    name: CharacterName
    department: Department
    subjects: list[Subject]
    img_path: str | PathLike
    punctuality: float = 1.0
    popularity: float = 1.0

@dataclass
class Prefect:
    id: str
    
    name: CharacterName
    post_name: str
    cls: Class
    img_path: str | PathLike
    duties: dict[str, list[str]]
    punctuality: float = 1.0
    popularity: float = 1.0


@dataclass
class Sensor:
    meta_data: SensorMeta
    img_path: str
    reading: LiveData | None = None

