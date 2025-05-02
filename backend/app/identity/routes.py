"""
Routes for the identity module.
"""
from flask import Blueprint

from .controller import IdentityController

# Create blueprints
auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
users_bp = Blueprint("users", __name__, url_prefix="/api/users")

# Auth routes
auth_bp.route("/login", methods=["POST"])(IdentityController.login)

# User routes
users_bp.route("", methods=["POST"])(IdentityController.register_user)
users_bp.route("", methods=["GET"])(IdentityController.get_all_users) 