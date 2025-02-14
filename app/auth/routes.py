from flask.blueprints import Blueprint

from app.auth.controller import AuthController

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

auth_bp.route("/login", methods=["POST"])(AuthController.login)
