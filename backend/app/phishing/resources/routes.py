from flask.blueprints import Blueprint
from .controller import ResourcesController

# Admin API routes
resources_bp = Blueprint('resources', __name__, url_prefix='/api/resources')
resources_bp.route('/', methods=['GET'])(ResourcesController.get_resources)
resources_bp.route('/', methods=['POST'])(ResourcesController.create_resource)
resources_bp.route('/<int:resource_id>', methods=['GET'])(ResourcesController.get_resource)
resources_bp.route('/scenario/<int:scenario_id>', methods=['GET'])(ResourcesController.get_resources_by_scenario)
resources_bp.route('/domain/<string:domain_name>', methods=['GET'])(ResourcesController.get_resources_by_domain)

# Public-facing routes for serving phishing content
# TODO: This should be in a separate file and should handle serving resources in a different way
#       It should track the interaction, and serve based on both the domain and the endpoint
phishing_bp = Blueprint('phishing', __name__, url_prefix='/p')
phishing_bp.route('/<string:domain_name>/<path:endpoint>', methods=['GET', 'POST'])(ResourcesController.serve_resource) 