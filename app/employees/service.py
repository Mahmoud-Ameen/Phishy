from app.employees.entitiy import Employee, Criticality
from app.employees.repository import EmployeeRepository


class EmployeeService:
    @staticmethod
    def get_employees() -> list[Employee]:
        return EmployeeRepository.get_employees()

    @staticmethod
    def create_employee(email: str, first_name: str, last_name: str, criticality: str, dept_name: str) -> Employee:
        """
        Create an employee
        :raises EmployeeAlreadyExists: if employee with email already exists
        :raises DepartmentDoesntExist: if department doesn't exist
        """ ""
        employee = Employee(email=email,
                            first_name=first_name,
                            last_name=last_name,
                            criticality=Criticality(criticality),
                            dept_name=dept_name)
        return EmployeeRepository.create_employee(employee)


class DepartmentService:
    @staticmethod
    def get_departments() -> list[str]:
        return EmployeeRepository.get_departments()

    @staticmethod
    def create_department(name: str) -> str:
        """
        Create a department
        :raises DepartmentAlreadyExists: if department already exists
        """ ""
        return EmployeeRepository.create_department(name)
