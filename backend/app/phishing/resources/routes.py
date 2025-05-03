from flask.blueprints import Blueprint
from .controller import ResourcesController

# Admin API routes
resources_bp = Blueprint('resources', __name__, url_prefix='/api/resources')
resources_bp.route('/', methods=['GET'])(ResourcesController.get_resources)
resources_bp.route('/', methods=['POST'])(ResourcesController.create_resource)
resources_bp.route('/<int:resource_id>', methods=['GET'])(ResourcesController.get_resource)
resources_bp.route('/scenario/<int:scenario_id>', methods=['GET'])(ResourcesController.get_resources_by_scenario)
resources_bp.route('/domain/<string:domain_name>', methods=['GET'])(ResourcesController.get_resources_by_domain)

