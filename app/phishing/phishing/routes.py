from flask import send_file
from flask.blueprints import Blueprint

tracking_bp = Blueprint("tracking", __name__, url_prefix="/phishing")


# track link clicks
@tracking_bp.route("/click/<tracking_key>")
def track_click(tracking_key):
    print("Link clicked", tracking_key)
    return "Are you supposed to open a random link?"


# track email opens
@tracking_bp.route("/openmail/<tracking_key>")
def track_open(tracking_key):
    print("Email opened", tracking_key)
    return send_file("./footer.gif", mimetype='image/gif')
