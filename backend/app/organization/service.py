"""
Service layer for organization operations.
"""
from .entity import Employee, Department, Criticality
from .repository import EmployeeRepository, DepartmentRepository
from app.core.exceptions import DepartmentDoesntExist, DepartmentAlreadyExists, EmployeeAlreadyExists


class OrganizationService:
    """Service for organization operations including employee and department management."""
    
    @staticmethod
    def get_all_employees() -> list[Employee]:
        """
        Get all employees.
        
        Returns:
            list[Employee]: List of all employee entities
        """
        return EmployeeRepository.get_all()
    
    @staticmethod
    def get_employee_by_email(email: str) -> Employee:
        """
        Get an employee by email.
        
        Args:
            email: Employee's email address
            
        Returns:
            Employee: The employee entity if found, None otherwise
        """
        return EmployeeRepository.get_by_email(email)
    
    @staticmethod
    def get_employees_by_department(dept_name: str) -> list[Employee]:
        """
        Get all employees in a department.
        
        Args:
            dept_name: Department name
            
        Returns:
            list[Employee]: List of employee entities in the department
            
        Raises:
            DepartmentDoesntExist: If department doesn't exist
        """
        department = DepartmentRepository.get_by_name(dept_name)
        if not department:
            raise DepartmentDoesntExist(f"Department '{dept_name}' doesn't exist")
            
        return EmployeeRepository.get_by_department(dept_name)
    
    @staticmethod
    def create_employee(email: str, first_name: str, last_name: str, criticality: str, dept_name: str) -> Employee:
        """
        Create a new employee.
        
        Args:
            email: Employee's email address
            first_name: Employee's first name
            last_name: Employee's last name
            criticality: Employee's criticality level (low, medium, high)
            dept_name: Department name
            
        Returns:
            Employee: The newly created employee entity
            
        Raises:
            EmployeeAlreadyExists: If an employee with the given email already exists
            DepartmentDoesntExist: If the department doesn't exist
            ValueError: If criticality is invalid
        """
        try:
            criticality_enum = Criticality(criticality)
        except ValueError:
            raise ValueError(f"Invalid criticality: {criticality}. Must be one of: {', '.join([c.value for c in Criticality])}")
        
        employee = Employee(
            email=email,
            first_name=first_name,
            last_name=last_name,
            criticality=criticality_enum,
            dept_name=dept_name
        )
        
        return EmployeeRepository.create(employee)
    
    @staticmethod
    def update_employee(email: str, first_name: str, last_name: str, criticality: str, dept_name: str) -> Employee:
        """
        Update an existing employee.
        
        Args:
            email: Employee's email address
            first_name: Employee's first name
            last_name: Employee's last name
            criticality: Employee's criticality level (low, medium, high)
            dept_name: Department name
            
        Returns:
            Employee: The updated employee entity
            
        Raises:
            ValueError: If the employee doesn't exist or criticality is invalid
            DepartmentDoesntExist: If the department doesn't exist
        """
        employee = EmployeeRepository.get_by_email(email)
        if not employee:
            raise ValueError(f"Employee with email {email} not found")
            
        try:
            criticality_enum = Criticality(criticality)
        except ValueError:
            raise ValueError(f"Invalid criticality: {criticality}. Must be one of: {', '.join([c.value for c in Criticality])}")
        
        updated_employee = Employee(
            email=email,
            first_name=first_name,
            last_name=last_name,
            criticality=criticality_enum,
            dept_name=dept_name
        )
        
        return EmployeeRepository.update(updated_employee)
    
    @staticmethod
    def delete_employee(email: str) -> None:
        """
        Delete an employee.
        
        Args:
            email: Employee's email address
            
        Raises:
            ValueError: If the employee doesn't exist
        """
        EmployeeRepository.delete(email)
    
    @staticmethod
    def get_all_departments() -> list[Department]:
        """
        Get all departments.
        
        Returns:
            list[Department]: List of all department entities
        """
        return DepartmentRepository.get_all()
    
    @staticmethod
    def get_department_by_name(name: str) -> Department:
        """
        Get a department by name.
        
        Args:
            name: Department name
            
        Returns:
            Department: The department entity if found, None otherwise
        """
        return DepartmentRepository.get_by_name(name)
    
    @staticmethod
    def create_department(name: str) -> Department:
        """
        Create a new department.
        
        Args:
            name: Department name
            
        Returns:
            Department: The newly created department entity
            
        Raises:
            DepartmentAlreadyExists: If a department with the given name already exists
        """
        return DepartmentRepository.create(name)
    
    @staticmethod
    def delete_department(name: str) -> None:
        """
        Delete a department.
        
        Args:
            name: Department name
            
        Raises:
            ValueError: If the department doesn't exist or has employees
        """
        DepartmentRepository.delete(name) 