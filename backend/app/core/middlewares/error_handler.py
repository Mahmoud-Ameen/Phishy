# libraries
import logging
from flask_jwt_extended import JWTManager

# application specific
from app.core.response import ApiResponse

logger = logging.getLogger(__name__)


def register_error_handlers(app):

    @app.errorhandler(404)
    def handle_not_found_error(e):
        logger.error(f"Resource not found: {e}")
        return ApiResponse.error("Resource not found", 404)

    @app.errorhandler(415)
    def handle_unsupported_media_type_error(e):
        logger.error(f"Unsupported media type: {e}")
        return ApiResponse.error("Unsupported media type", 415)

    @app.errorhandler(400)
    def handle_bad_request_error(e):
        logger.error(f"Bad request: {e}")
        return ApiResponse.error("Bad request", 400)

    @app.errorhandler(Exception)
    def handle_generic_exception(e: Exception):
        logger.error(f"Unexpected error: {e}", e.__traceback__)
        return ApiResponse.error("An unexpected error occurred", 500)

    # region JWT Error Handlers
    # Force Flask-JWT-Extended to use our custom error handling
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def custom_unauthorized_response(err_msg):
        """Handles missing token errors (NoAuthorizationError)"""
        logger.error(f"JWT Unauthorized: {err_msg}")
        return ApiResponse.error(err_msg, 401)

    @jwt.expired_token_loader
    def custom_expired_token_response(jwt_header, jwt_payload):
        """Handles expired token errors"""
        logger.error("JWT Token has expired")
        return ApiResponse.error("Token has expired", 401)

    @jwt.invalid_token_loader
    def custom_invalid_token_response(err_msg):
        """Handles invalid token errors"""
        logger.error(f"JWT Invalid Token: {err_msg}")
        return ApiResponse.error("Invalid authentication token", 401)
    # endregion

