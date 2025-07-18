from PyQt6.QtCore import pyqtSignal, pyqtBoundSignal
from dataclasses import dataclass
from typing import Callable

@dataclass
class Time:
    sec: float
    min: int
    hour: int

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
class Department:
    id: str
    
    name: str

