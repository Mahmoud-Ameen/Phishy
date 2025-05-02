"""
Identity models for authentication and authorization.
"""
import enum
from sqlalchemy.orm import Mapped
from app.extensions import db


class UserRole(enum.Enum):
    """Defines roles for users in the system."""
    ADMIN = "admin"
    READ_ONLY = "read-only"


class UserModel(db.Model):
    """User model representing system administrators and operators."""
    __tablename__ = "users"
    email: Mapped[str] = db.Column(db.String(255), primary_key=True)
    role: UserRole = db.Column(db.Enum(UserRole, values_callable=lambda x: [e.value for e in x]), nullable=False)
    first_name: str = db.Column(db.String(255), nullable=False)
    last_name: str = db.Column(db.String(255), nullable=False)
    password: str = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        """Convert user model to dictionary."""
        return {
            "email": self.email,
            "role": self.role.value,
            "first_name": self.first_name,
            "last_name": self.last_name
        } 