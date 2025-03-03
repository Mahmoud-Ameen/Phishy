from flask import Blueprint, request
from .controller import UserController

users_bp = Blueprint("users", __name__)

users_bp.route("/api/users", methods=["POST"])(UserController.register_user)
