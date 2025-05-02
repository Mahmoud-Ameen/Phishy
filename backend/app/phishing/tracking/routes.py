from flask import Blueprint, request, send_file, current_app
from .service import TrackingService
import os
import logging

tracking_bp = Blueprint("tracking", __name__, url_prefix="/api/tracking")
logger = logging.getLogger(__name__)

# Track link clicks
@tracking_bp.route("/click/<tracking_key>")
def track_click(tracking_key):
    """
    Track link clicks and redirect to the appropriate landing page
    """
    try:
        # Get client info
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        
        # Record the click
        result = TrackingService.record_click(
            tracking_key=tracking_key,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Here you would typically redirect to the landing page based on the scenario
        return "Link clicked. This would typically redirect to a phishing landing page."
    except Exception as e:
        logger.error(f"Error tracking link click: {str(e)}")
        return "Error processing your request", 500

# Track email opens via tracking pixel
@tracking_bp.route("/open/<tracking_key>")
def track_open(tracking_key: str):
    """
    Track email opens by serving a 1x1 transparent GIF.
    The image will always be served, even for invalid tracking keys.
    """
    print(f"Tracking open for key: {tracking_key}")
    try:
        # Get client info
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')

        # Try to record the interaction if the tracking key is valid
        TrackingService.record_open(
            tracking_key=tracking_key,
            ip_address=ip_address,
            user_agent=user_agent
        )
    except Exception as e:
        logger.error(f"Error tracking email open: {str(e)}")
        # Continue to serve the image even if tracking fails

    # Always serve the 1x1 transparent GIF
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pixel_path = os.path.join(current_dir, "transparent.gif")
    return send_file(pixel_path, mimetype='image/gif')

# Record form submissions from landing pages
@tracking_bp.route("/submit/<tracking_key>", methods=["POST"])
def track_form_submission(tracking_key):
    """
    Record a form submission from a phishing landing page
    """
    try:
        # Get client info
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        form_data = request.form.to_dict()
        
        # Record the submission
        TrackingService.record_submission(
            tracking_key=tracking_key,
            ip_address=ip_address,
            user_agent=user_agent,
            form_data=form_data
        )
        
        return "Form submitted. Thank you."
    except Exception as e:
        logger.error(f"Error tracking form submission: {str(e)}")
        return "Error processing your request", 500 