from flask import Blueprint, request, send_file, current_app
from .service import TrackingService
import os
import logging

tracking_bp = Blueprint('tracking', __name__)
logger = logging.getLogger(__name__)

@tracking_bp.route('/api/tracking/open/<tracking_key>')
def track_email_open(tracking_key: str):
    """
    Track email opens by serving a 1x1 transparent GIF.
    The image will always be served, even for invalid tracking keys.
    """
    try:
        # Get client info
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')

        # Try to record the interaction if the tracking key is valid
        target = TrackingService.get_target_by_tracking_key(tracking_key)
        if target:
            TrackingService.record_email_open(
                tracking_key=tracking_key,
                ip_address=ip_address,
                user_agent=user_agent
            )
    except Exception as e:
        logger.error(f"Error tracking email open: {str(e)}")
        # Continue to serve the image even if tracking fails

    # Always serve the 1x1 transparent GIF
    transparent_gif_path = os.path.join(current_app.root_path, 'phishing', 'tracking', 'transparent.gif')
    return send_file(transparent_gif_path, mimetype='image/gif') 