
from dataclasses import dataclass
from os import PathLike


@dataclass
class BT_Device:
    name: str
    addr: str
    port: int = 1234


@dataclass
class CharacterName:
    sur: str
    first: str
    middle: str
    abrev: str
    other: str | None = None
    nick: str | None = None

@dataclass
class PrefectDuty:
    morning: bool
    labour: bool

@dataclass
class Class:
    id: str
    
    level_name: str
    class_name: str
    name: str

@dataclass
class Subject:
    id: str
    
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

