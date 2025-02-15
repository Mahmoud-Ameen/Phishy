from flask.blueprints import Blueprint
from .controller import CampaignsController

campaigns_bp = Blueprint('campaigns', __name__, url_prefix='/api/campaigns')

# Get all campaigns
campaigns_bp.route('/', methods=['GET'])(CampaignsController.get_campaigns)
# Start a campaign
campaigns_bp.route('/', methods=['POST'])(CampaignsController.start_campaign)
