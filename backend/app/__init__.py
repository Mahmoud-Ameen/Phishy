from flask import Flask
from flask_cors import CORS

# app specific
from app.core.middlewares import register_error_handlers
from .extensions import db, jwt
from .config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.url_map.strict_slashes = False

    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    register_error_handlers(app)

    # Register user blueprints
    from app.identity.routes import users_bp, auth_bp
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)

    # Register employees and departments blueprints
    from app.organization.routes import employees_bp, departments_bp
    app.register_blueprint(employees_bp)
    app.register_blueprint(departments_bp)

    # Register templates blueprints
    from app.phishing.scenarios.routes import templates_bp
    app.register_blueprint(templates_bp)

    # Register scenarios blueprints
    from app.phishing.scenarios.routes import scenarios_bp
    app.register_blueprint(scenarios_bp)

    # Register domains blueprints
    from app.phishing.domains.routes import domains_bp
    app.register_blueprint(domains_bp)

    # Register resources blueprints
    from app.phishing.resources.routes import resources_bp
    app.register_blueprint(resources_bp)
    
    # Register phishing blueprints
    from app.phishing.resources.routes import phishing_bp
    app.register_blueprint(phishing_bp)

    # Register campaigns blueprints
    from app.campaigns.routes import campaigns_bp
    app.register_blueprint(campaigns_bp)

    # Register tracking blueprints
    from app.phishing.tracking.routes import tracking_bp
    app.register_blueprint(tracking_bp)

    @app.route('/')
    def index():
        return "Hello, World!"

    with app.app_context():
        db.create_all()

    return app
