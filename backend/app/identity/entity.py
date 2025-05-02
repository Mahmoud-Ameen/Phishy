"""
Entity objects for the identity module.
"""
import enum
from dataclasses import dataclass


class UserRole(enum.Enum):
    """Defines roles for users in the system."""
    ADMIN = "admin"
    READ_ONLY = "read-only"


@dataclass
class User:
    """User entity representing system administrators and operators."""
    email: str
    role: UserRole
    first_name: str
    last_name: str
    password_hash: str

    def to_dict(self) -> dict:
        """Convert user entity to dictionary."""
        return {
            "email": self.email,
            "role": self.role.value,
            "first_name": self.first_name,
            "last_name": self.last_name,
        } 