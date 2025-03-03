from flask.blueprints import Blueprint
from app.company.employees.controller import EmployeesController, DepartmentsController

employees_bp = Blueprint('employees', __name__, url_prefix='/api/employees')

# get all employees
employees_bp.route('/', methods=['GET'])(EmployeesController.get_employees)

# create an employee
employees_bp.route('/', methods=['POST'])(EmployeesController.create_employee)

departments_bp = Blueprint('departments', __name__, url_prefix='/api/departments')

# get all departments
departments_bp.route('/', methods=['GET'])(DepartmentsController.get_departments)

# create a department
departments_bp.route('/', methods=['POST'])(DepartmentsController.create_department)

