"""
Entity objects for the organization module.
"""
from dataclasses import dataclass
from enum import Enum


class Criticality(str, Enum):
    """Criticality levels for employees in terms of phishing risk."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Employee:
    """Employee entity representing company employees."""
    email: str
    first_name: str
    last_name: str
    criticality: Criticality
    dept_name: str

    def to_dict(self) -> dict:
        """Convert employee entity to dictionary."""
        return {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "criticality": self.criticality.value,
            "dept_name": self.dept_name
        }


@dataclass 
class Department:
    """Department entity representing company departments."""
    name: str
    
    def to_dict(self) -> dict:
        """Convert department entity to dictionary."""
        return {
            "name": self.name
        } 