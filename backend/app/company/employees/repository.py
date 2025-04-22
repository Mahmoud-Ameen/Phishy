from sqlalchemy.exc import IntegrityError
from .models import EmployeeModel, DepartmentModel
from .entitiy import Criticality, Employee, Department
from app import db
from app.core.exceptions import (
    DepartmentDoesntExist, 
    DepartmentAlreadyExists, 
    EmployeeAlreadyExists
)


class EmployeeRepository:
    @staticmethod
    def get_employees() -> list[Employee]:
        """ Get all employees """" """
        employees: list[EmployeeModel] = EmployeeModel.query.all()
        return [EmployeeRepository._model_to_entity(employee) for employee in employees]

    @staticmethod
    def create_employee(employee: Employee):
        """
        Create an employee 
        :param employee: Employee entity
        :return: Employee entity
        :raises EmployeeAlreadyExists: if employee with email already exists
        :raises DepartmentDoesntExist: if department doesn't exist
        """ ""
        employee = EmployeeModel(
            email=employee.email,
            first_name=employee.first_name,
            last_name=employee.last_name,
            criticality=employee.criticality,
            dept_name=employee.dept_name
        )
        try:
            # check if department exists
            department = DepartmentModel.query.filter_by(name=employee.dept_name).first()
            if not department:
                raise DepartmentDoesntExist(f"Department '{employee.dept_name}' doesn't exist")

            # save employee to db
            db.session.add(employee)
            db.session.commit()
            return EmployeeRepository._model_to_entity(employee)
        except IntegrityError as e:
            db.session.rollback()
            raise EmployeeAlreadyExists(f"Employee with email '{employee.email}' already exists")

    @staticmethod
    def get_departments() -> list[Department]:
        departments = DepartmentModel.query.all()
        return [EmployeeRepository.department_model_to_entity(dept) for dept in departments]

    @staticmethod
    def create_department(name: str) -> Department:
        """
        Create a department 
        :param name: department name    
        :return: department name
        :raises DepartmentAlreadyExists: if department already exists
        """ ""

        department = DepartmentModel(name=name)
        try:
            db.session.add(department)
            db.session.commit()
            return EmployeeRepository.department_model_to_entity(department)
        except IntegrityError:
            db.session.rollback()
            raise DepartmentAlreadyExists(f"Department '{name}' already exists")

    @staticmethod
    def _model_to_entity(employee: EmployeeModel) -> Employee:
        return Employee(
            email=employee.email,
            first_name=employee.first_name,
            last_name=employee.last_name,
            criticality=Criticality(employee.criticality.value),
            dept_name=employee.dept_name
        )

    @staticmethod
    def department_model_to_entity(department: DepartmentModel) -> Department:
        return Department(name=department.name)