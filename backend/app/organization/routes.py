"""
Routes for the organization module.
"""
from flask import Blueprint

from .controller import EmployeeController, DepartmentController

# Create blueprints
employees_bp = Blueprint('employees', __name__, url_prefix='/api/employees')
departments_bp = Blueprint('departments', __name__, url_prefix='/api/departments')

# Employee routes
employees_bp.route('', methods=['GET'])(EmployeeController.get_all_employees)
employees_bp.route('', methods=['POST'])(EmployeeController.create_employee)
employees_bp.route('/<email>', methods=['GET'])(EmployeeController.get_employee)
employees_bp.route('/<email>', methods=['PUT'])(EmployeeController.update_employee)
employees_bp.route('/<email>', methods=['DELETE'])(EmployeeController.delete_employee)

# Department routes
departments_bp.route('', methods=['GET'])(DepartmentController.get_all_departments)
departments_bp.route('', methods=['POST'])(DepartmentController.create_department)
departments_bp.route('/<name>', methods=['GET'])(DepartmentController.get_department)
departments_bp.route('/<name>', methods=['DELETE'])(DepartmentController.delete_department) 