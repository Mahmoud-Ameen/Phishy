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

    def to_dict(self):
        return {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "criticality": self.criticality.value,
            "dept_name": self.dept_name
        }

@dataclass 
class Department:
    name: str
    
    def to_dict(self):
        return {
            "name": self.name
        }