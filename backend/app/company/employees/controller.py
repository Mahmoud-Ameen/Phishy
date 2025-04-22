from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.core.response import ApiResponse
from .entitiy import Employee
from .service import EmployeeService, DepartmentService
from app.core.exceptions import EmployeeAlreadyExists, DepartmentDoesntExist, DepartmentAlreadyExists
from app.core.middlewares import admin_required
from .schemas import EmployeeCreateSchema, DepartmentCreateSchema


class EmployeesController:
    @staticmethod
    @jwt_required()
    def get_employees():
        employees: list[Employee] = EmployeeService.get_employees()
        data = [emp.to_dict() for emp in employees]
        return ApiResponse.success({"employees": data})

    @staticmethod
    def create_employee():
        try:
            data = request.get_json()
            EmployeeCreateSchema().load(data)
            employee = EmployeeService.create_employee(**data)
            return ApiResponse.success(
                {"employee": employee.to_dict()}, 
                "Employee created successfully"
            )
        except ValidationError as e:
            return ApiResponse.error("Validation error", 400, e.messages)
        except EmployeeAlreadyExists:
            return ApiResponse.error("Employee already exists", 409)
        except DepartmentDoesntExist:
            return ApiResponse.error("Department doesn't exist", 400)


class DepartmentsController:
    @staticmethod
    @jwt_required()
    def get_departments():
        departments = DepartmentService.get_departments()
        return ApiResponse.success({"departments": [d.to_dict() for d in departments]})

    @staticmethod
    @jwt_required()
    @admin_required
    def create_department():
        try:
            data = DepartmentCreateSchema().load(request.json)
            department = DepartmentService.create_department(data['name'])
            return ApiResponse.success(
                {"department": department.to_dict()}, 
                "Department created successfully"
            )
        except ValidationError as e:
            return ApiResponse.error("Validation error", 400, e.messages)
        except DepartmentAlreadyExists:
            return ApiResponse.error("Department already exists", 409)
