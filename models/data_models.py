
from dataclasses import dataclass
from PyQt6.QtCore import pyqtBoundSignal

@dataclass
class Time:
    hour: int
    min: int
    sec: float

@dataclass
class LiveData:
    data_signal: pyqtBoundSignal

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
class Department:
    id: str
    
    name: str

