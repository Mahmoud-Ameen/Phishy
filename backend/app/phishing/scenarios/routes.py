from flask.blueprints import Blueprint
from .controller import TemplatesController, ScenariosController, DomainsController

# Templates routes
templates_bp = Blueprint('templates', __name__, url_prefix='/api/templates')
templates_bp.route('/', methods=['GET'])(TemplatesController.get_templates)
templates_bp.route('/', methods=['POST'])(TemplatesController.create_template)

# Scenarios routes
scenarios_bp = Blueprint('scenarios', __name__, url_prefix='/api/scenarios')
scenarios_bp.route('/', methods=['GET'])(ScenariosController.get_scenarios)
scenarios_bp.route('/', methods=['POST'])(ScenariosController.create_scenario)

# Domains routes
domains_bp = Blueprint('domains', __name__, url_prefix='/api/domains')
domains_bp.route('/', methods=['GET'])(DomainsController.get_domains)
domains_bp.route('/', methods=['POST'])(DomainsController.create_domain)
