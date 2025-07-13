from PyQt6.QtCore import pyqtSignal, pyqtBoundSignal
from dataclasses import dataclass
from os import PathLike
from typing import Callable


@dataclass
class BT_Device:
    name: str
    addr: str
    port: int = 1234


@dataclass
class LiveData:
    data_signal: pyqtBoundSignal
    data_func: Callable

@dataclass
class CharacterName:
    sur: str
    first: str
    middle: str
    abrev: str
    other: str | None = None

@dataclass
class SensorMeta:
    sensor_type: str
    model: str
    version: str
    developer: str

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
    duties: list[str]
    punctuality: float = 1.0
    popularity: float = 1.0


@dataclass
class Sensor:
    meta_data: SensorMeta
    img_path: str
    reading: LiveData = LiveData(lambda: "")

