# libraries
import logging
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt import ExpiredSignatureError
from werkzeug.exceptions import HTTPException

# application specific
from .exceptions import AppException
from .response import ApiResponse

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(AppException)
    def handle_app_exception(error):
        logger.error(f"AppException: {error.message}")
        return ApiResponse.error(error.message, error.status_code)

    @app.errorhandler(404)
    def handle_not_found(error=None):
        logger.error("Resource not found")
        return ApiResponse.error("Resource not found", 404)

    @app.errorhandler(NoAuthorizationError)
    def handle_no_authorization_error(e):
        logger.error("Missing or invalid authentication token")
        return ApiResponse.error("Missing or invalid authentication token", 401)

    @app.errorhandler(ExpiredSignatureError)
    def handle_expired_token_error(e):
        logger.error("Token has expired")
        return ApiResponse.error("Token has expired", 401)

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        if isinstance(e, HTTPException):
            logger.error(f"HTTPException: {e.description}")
            return ApiResponse.error(e.description, e.code)
        logger.error("An unexpected error occurred")
        return ApiResponse.error("An unexpected error occurred", 500)