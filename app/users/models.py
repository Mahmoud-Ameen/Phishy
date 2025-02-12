# libraries
import enum
from typing import Dict, Optional, Any
from werkzeug.security import generate_password_hash, check_password_hash

# app specific
from ..extensions import db


class UserRole(enum.Enum):
    ADMIN = "admin"
    READ_ONLY = "read-only"


class User(db.Model):
    email: str = db.Column(db.String(255), primary_key=True)
    role: UserRole = db.Column(db.Enum(UserRole), nullable=False)
    first_name: str = db.Column(db.String(255), nullable=False)
    last_name: str = db.Column(db.String(255), nullable=False)
    password: str = db.Column(db.String(255), nullable=False)

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "email": self.email,
            "role": self.role.value,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
