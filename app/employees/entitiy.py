from dataclasses import dataclass
from enum import Enum


class Criticality(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Employee:
    email: str
    first_name: str
    last_name: str
    criticality: Criticality
    dept_name: str
