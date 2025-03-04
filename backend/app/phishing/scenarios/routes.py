from flask.blueprints import Blueprint
from .controller import TemplatesController

templates_bp = Blueprint('templates', __name__, url_prefix='/api/templates')

# Get all templates
templates_bp.route('/', methods=['GET'])(TemplatesController.get_templates)

# Create a template
templates_bp.route('/', methods=['POST'])(TemplatesController.create_template)
