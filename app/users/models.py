# libraries
import enum
from sqlalchemy.orm import Mapped

# app specific
from ..extensions import db


class UserRole(enum.Enum):
    ADMIN = "admin"
    READ_ONLY = "read-only"


class UserModel(db.Model):
    __tablename__ = "users"
    email: Mapped[str] = db.Column(db.String(255), primary_key=True)
    role: UserRole = db.Column(db.Enum(UserRole, values_callable=lambda x: [e.value for e in x]), nullable=False)
    first_name: str = db.Column(db.String(255), nullable=False)
    last_name: str = db.Column(db.String(255), nullable=False)
    password: str = db.Column(db.String(255), nullable=False)
