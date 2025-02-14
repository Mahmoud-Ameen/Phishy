from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.to_dict()
