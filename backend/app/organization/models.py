"""
Organization domain models for departments and employees.
"""
import enum
from app.extensions import db


class DepartmentModel(db.Model):
    """Department model representing company departments."""
    __tablename__ = "departments"
    name: str = db.Column(db.String(255), primary_key=True)
    employees = db.relationship("EmployeeModel", backref="department", lazy=True)
    
    def to_dict(self):
        """Convert department model to dictionary."""
        return {
            "name": self.name
        }


class Criticality(enum.Enum):
    """Criticality levels for employees in terms of phishing risk."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class EmployeeModel(db.Model):
    """Employee model representing company employees."""
    __tablename__ = "employees"
    email: str = db.Column(db.String(255), primary_key=True)
    first_name: str = db.Column(db.String(255), nullable=False)
    last_name: str = db.Column(db.String(255), nullable=False)
    criticality: Criticality = db.Column(db.Enum(Criticality, values_callable=lambda x: [e.value for e in x]),
                                         nullable=False)
    dept_name: str = db.Column(db.String(255), db.ForeignKey("departments.name"), nullable=False)
    
    def to_dict(self):
        """Convert employee model to dictionary."""
        return {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "criticality": self.criticality.value,
            "dept_name": self.dept_name
        } 