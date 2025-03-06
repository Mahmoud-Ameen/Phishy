from flask.blueprints import Blueprint
from .controller import DomainsController

domains_bp = Blueprint('domains', __name__, url_prefix='/api/domains')
domains_bp.route('/', methods=['GET'])(DomainsController.get_domains)
domains_bp.route('/', methods=['POST'])(DomainsController.create_domain) 