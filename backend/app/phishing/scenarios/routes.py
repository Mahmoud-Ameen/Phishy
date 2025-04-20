from flask.blueprints import Blueprint
from .controller import TemplatesController, ScenariosController

# Templates routes
templates_bp = Blueprint('templates', __name__, url_prefix='/api/templates')
templates_bp.route('/', methods=['GET'])(TemplatesController.get_templates)
templates_bp.route('/', methods=['POST'])(TemplatesController.create_template)
templates_bp.route('/<int:template_id>', methods=['PUT'])(TemplatesController.update_template)
templates_bp.route('/<int:template_id>', methods=['DELETE'])(TemplatesController.delete_template)

# Scenarios routes
scenarios_bp = Blueprint('scenarios', __name__, url_prefix='/api/scenarios')
scenarios_bp.route('/', methods=['GET'])(ScenariosController.get_scenarios)
scenarios_bp.route('/', methods=['POST'])(ScenariosController.create_scenario)
