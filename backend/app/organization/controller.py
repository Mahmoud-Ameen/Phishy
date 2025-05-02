"""
Controllers for organization module handling HTTP requests.
"""
from flask import request
from marshmallow import ValidationError

from .service import OrganizationService
from app.core.exceptions import DepartmentDoesntExist, DepartmentAlreadyExists, EmployeeAlreadyExists
from app.core.middlewares import admin_required
from app.core.response import ApiResponse
from .schemas import (
    EmployeeCreateSchema, 
    EmployeeUpdateSchema,
    EmployeeResponseSchema,
    DepartmentCreateSchema,
    DepartmentResponseSchema
)


class EmployeeController:
    """Controller handling employee-related HTTP requests."""
    
    @staticmethod
    @admin_required
    def create_employee():
        """
        Create a new employee (admin only).
        
        Returns:
            Response: JSON response with the new employee data or error
        """
        try:
            data = EmployeeCreateSchema().load(request.json)
        except ValidationError as validation_error:
            return ApiResponse.error("Invalid request body", 400, validation_error.messages)
            
        try:
            employee = OrganizationService.create_employee(
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                criticality=data['criticality'],
                dept_name=data['dept_name']
            )
            return ApiResponse.success({"employee": EmployeeResponseSchema().dump(employee.to_dict())})
        except EmployeeAlreadyExists as e:
            return ApiResponse.error(str(e), 400)
        except DepartmentDoesntExist as e:
            return ApiResponse.error(str(e), 400)
        except ValueError as e:
            return ApiResponse.error(str(e), 400)
    
    @staticmethod
    def get_all_employees():
        """
        Get all employees.
        
        Returns:
            Response: JSON response with list of employees
        """
        employees = OrganizationService.get_all_employees()
        return ApiResponse.success({"employees": [EmployeeResponseSchema().dump(e.to_dict()) for e in employees]})
    
    @staticmethod
    def get_employee(email):
        """
        Get an employee by email.
        
        Args:
            email: Employee's email address
            
        Returns:
            Response: JSON response with employee data or error
        """
        employee = OrganizationService.get_employee_by_email(email)
        if not employee:
            return ApiResponse.error(f"Employee with email {email} not found", 404)
            
        return ApiResponse.success({"employee": EmployeeResponseSchema().dump(employee.to_dict())})
    
    @staticmethod
    @admin_required
    def update_employee(email):
        """
        Update an employee (admin only).
        
        Args:
            email: Employee's email address
            
        Returns:
            Response: JSON response with updated employee data or error
        """
        try:
            data = EmployeeUpdateSchema().load(request.json)
        except ValidationError as validation_error:
            return ApiResponse.error("Invalid request body", 400, validation_error.messages)
            
        try:
            employee = OrganizationService.update_employee(
                email=email,
                first_name=data['first_name'],
                last_name=data['last_name'],
                criticality=data['criticality'],
                dept_name=data['dept_name']
            )
            return ApiResponse.success({"employee": EmployeeResponseSchema().dump(employee.to_dict())})
        except ValueError as e:
            return ApiResponse.error(str(e), 400)
        except DepartmentDoesntExist as e:
            return ApiResponse.error(str(e), 400)
    
    @staticmethod
    @admin_required
    def delete_employee(email):
        """
        Delete an employee (admin only).
        
        Args:
            email: Employee's email address
            
        Returns:
            Response: JSON response with success or error
        """
        try:
            OrganizationService.delete_employee(email)
            return ApiResponse.success(message=f"Employee with email {email} deleted successfully")
        except ValueError as e:
            return ApiResponse.error(str(e), 404)


class DepartmentController:
    """Controller handling department-related HTTP requests."""
    
    @staticmethod
    @admin_required
    def create_department():
        """
        Create a new department (admin only).
        
        Returns:
            Response: JSON response with the new department data or error
        """
        try:
            data = DepartmentCreateSchema().load(request.json)
        except ValidationError as validation_error:
            return ApiResponse.error("Invalid request body", 400, validation_error.messages)
            
        try:
            department = OrganizationService.create_department(name=data['name'])
            return ApiResponse.success({"department": DepartmentResponseSchema().dump(department.to_dict())})
        except DepartmentAlreadyExists as e:
            return ApiResponse.error(str(e), 400)
    
    @staticmethod
    def get_all_departments():
        """
        Get all departments.
        
        Returns:
            Response: JSON response with list of departments
        """
        departments = OrganizationService.get_all_departments()
        return ApiResponse.success({"departments": [DepartmentResponseSchema().dump(d.to_dict()) for d in departments]})
    
    @staticmethod
    def get_department(name):
        """
        Get a department by name.
        
        Args:
            name: Department name
            
        Returns:
            Response: JSON response with department data or error
        """
        department = OrganizationService.get_department_by_name(name)
        if not department:
            return ApiResponse.error(f"Department with name {name} not found", 404)
            
        return ApiResponse.success({"department": DepartmentResponseSchema().dump(department.to_dict())})
    
    @staticmethod
    @admin_required
    def delete_department(name):
        """
        Delete a department (admin only).
        
        Args:
            name: Department name
            
        Returns:
            Response: JSON response with success or error
        """
        try:
            OrganizationService.delete_department(name)
            return ApiResponse.success(message=f"Department with name {name} deleted successfully")
        except ValueError as e:
            return ApiResponse.error(str(e), 400) 