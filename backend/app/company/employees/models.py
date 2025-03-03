import enum
from app.extensions import db


class DepartmentModel(db.Model):
    __tablename__ = "departments"
    name: str = db.Column(db.String(255), primary_key=True)
    employees = db.relationship("EmployeeModel", backref="department", lazy=True)


class Criticality(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class EmployeeModel(db.Model):
    __tablename__ = "employees"
    email: str = db.Column(db.String(255), primary_key=True)
    first_name: str = db.Column(db.String(255), nullable=False)
    last_name: str = db.Column(db.String(255), nullable=False)
    criticality: Criticality = db.Column(db.Enum(Criticality, values_callable=lambda x: [e.value for e in x]),
                                         nullable=False)
    dept_name: str = db.Column(db.String(255), db.ForeignKey("departments.name"), nullable=False)
