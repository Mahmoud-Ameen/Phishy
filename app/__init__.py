from flask import Flask

# app specific
from app.middlewares.error_handler import register_error_handlers
from .extensions import db, jwt
from .config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    register_error_handlers(app)

    # Register blueprints
    from app.users.routes import users_bp
    app.register_blueprint(users_bp)
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    return app
