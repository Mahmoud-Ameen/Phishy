from flask import Flask

# app specific
from .core.error_handler import register_error_handlers
from .extensions import db
from .config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    register_error_handlers(app)

    # Register blueprints

    return app
