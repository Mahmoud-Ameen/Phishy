from flask import Blueprint

# Blueprint for any routes that control the email sending process
mailer_bp = Blueprint("mailer", __name__, url_prefix="/api/mailer")
