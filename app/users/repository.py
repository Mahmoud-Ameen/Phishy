from typing import Any

# app specific
from .models import User
from ..extensions import db


class UserRepository:
    @staticmethod
    def create(email: str, role: str, first_name: str, last_name: str, password: str) -> dict[str, Any]:
        user = User(email=email, role=role, first_name=first_name, last_name=last_name)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return user.to_dict()

    @staticmethod
    def get_by_email(email: str) -> dict[str, Any]:
        return User.query.filter_by(email=email).first()
    