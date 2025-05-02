"""
Repository for organization data access.
"""
from sqlalchemy.exc import IntegrityError
from .models import EmployeeModel, DepartmentModel
from .entity import Criticality, Employee, Department
from app.extensions import db
from app.core.exceptions import (
    DepartmentDoesntExist, 
    DepartmentAlreadyExists, 
    EmployeeAlreadyExists
)


class EmployeeRepository:
    """Repository for employee data access operations."""
    
    @staticmethod
    def get_all() -> list[Employee]:
        """Get all employees."""
        employees = EmployeeModel.query.all()
        return [EmployeeRepository._model_to_entity(employee) for employee in employees]
        
    @staticmethod
    def get_by_email(email: str) -> Employee:
        """Get an employee by email."""
        employee = EmployeeModel.query.filter_by(email=email).first()
        if not employee:
            return None
        return EmployeeRepository._model_to_entity(employee)
        
    @staticmethod
    def get_by_department(dept_name: str) -> list[Employee]:
        """Get all employees in a department."""
        employees = EmployeeModel.query.filter_by(dept_name=dept_name).all()
        return [EmployeeRepository._model_to_entity(employee) for employee in employees]

    @staticmethod
    def create(employee: Employee) -> Employee:
        """
        Create an employee.
        
        Args:
            employee: Employee entity
            
        Returns:
            Employee: Created employee entity
            
        Raises:
            EmployeeAlreadyExists: If employee with email already exists
            DepartmentDoesntExist: If department doesn't exist
        """
        employee_model = EmployeeModel(
            email=employee.email,
            first_name=employee.first_name,
            last_name=employee.last_name,
            criticality=employee.criticality,
            dept_name=employee.dept_name
        )
        try:
            # Check if department exists
            department = DepartmentModel.query.filter_by(name=employee.dept_name).first()
            if not department:
                raise DepartmentDoesntExist(f"Department '{employee.dept_name}' doesn't exist")

            # Save employee to db
            db.session.add(employee_model)
            db.session.commit()
            return EmployeeRepository._model_to_entity(employee_model)
        except IntegrityError:
            db.session.rollback()
            raise EmployeeAlreadyExists(f"Employee with email '{employee.email}' already exists")
            
    @staticmethod
    def update(employee: Employee) -> Employee:
        """Update an employee."""
        employee_model = EmployeeModel.query.get(employee.email)
        if not employee_model:
            raise ValueError(f"Employee with email {employee.email} not found")
            
        # Check if department exists if it's changed
        if employee_model.dept_name != employee.dept_name:
            department = DepartmentModel.query.filter_by(name=employee.dept_name).first()
            if not department:
                raise DepartmentDoesntExist(f"Department '{employee.dept_name}' doesn't exist")
        
        employee_model.first_name = employee.first_name
        employee_model.last_name = employee.last_name
        employee_model.criticality = employee.criticality
        employee_model.dept_name = employee.dept_name
        
        db.session.commit()
        return EmployeeRepository._model_to_entity(employee_model)
        
    @staticmethod
    def delete(email: str) -> None:
        """Delete an employee."""
        employee = EmployeeModel.query.get(email)
        if not employee:
            raise ValueError(f"Employee with email {email} not found")
            
        db.session.delete(employee)
        db.session.commit()

    @staticmethod
    def _model_to_entity(employee: EmployeeModel) -> Employee:
        """Convert an EmployeeModel to an Employee entity."""
        return Employee(
            email=employee.email,
            first_name=employee.first_name,
            last_name=employee.last_name,
            criticality=Criticality(employee.criticality.value),
            dept_name=employee.dept_name
        )


class DepartmentRepository:
    """Repository for department data access operations."""
    
    @staticmethod
    def get_all() -> list[Department]:
        """Get all departments."""
        departments = DepartmentModel.query.all()
        return [DepartmentRepository._model_to_entity(dept) for dept in departments]
        
    @staticmethod
    def get_by_name(name: str) -> Department:
        """Get a department by name."""
        department = DepartmentModel.query.filter_by(name=name).first()
        if not department:
            return None
        return DepartmentRepository._model_to_entity(department)

    @staticmethod
    def create(name: str) -> Department:
        """
        Create a department.
        
        Args:
            name: Department name
            
        Returns:
            Department: Created department entity
            
        Raises:
            DepartmentAlreadyExists: If department already exists
        """
        department = DepartmentModel(name=name)
        try:
            db.session.add(department)
            db.session.commit()
            return DepartmentRepository._model_to_entity(department)
        except IntegrityError:
            db.session.rollback()
            raise DepartmentAlreadyExists(f"Department '{name}' already exists")
            
    @staticmethod
    def delete(name: str) -> None:
        """Delete a department."""
        department = DepartmentModel.query.get(name)
        if not department:
            raise ValueError(f"Department with name {name} not found")
            
        # Check if there are employees in this department
        employees = EmployeeModel.query.filter_by(dept_name=name).first()
        if employees:
            raise ValueError(f"Cannot delete department {name} because it has employees")
            
        db.session.delete(department)
        db.session.commit()

    @staticmethod
    def _model_to_entity(department: DepartmentModel) -> Department:
        """Convert a DepartmentModel to a Department entity."""
        return Department(name=department.name) 