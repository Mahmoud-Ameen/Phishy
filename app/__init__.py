from flask import Flask

# app specific
from app.core.middlewares import register_error_handlers
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
    from app.company.users.routes import users_bp
    app.register_blueprint(users_bp)
    from app.company.auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    from app.company.employees.routes import employees_bp, departments_bp
    app.register_blueprint(employees_bp)
    app.register_blueprint(departments_bp)

    from app.phishing.templates.routes import templates_bp
    app.register_blueprint(templates_bp)

    with app.app_context():
        db.create_all()

    return app
