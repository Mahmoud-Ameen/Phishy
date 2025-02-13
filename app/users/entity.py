import enum
from dataclasses import dataclass

from werkzeug.security import generate_password_hash, check_password_hash


class UserRole(enum.Enum):
    ADMIN = "admin"
    READ_ONLY = "read-only"


@dataclass
class UserEntity:
    email: str
    role: UserRole
    first_name: str
    last_name: str
    password_hash: str

    def to_dict(self) -> object:
        return {
            "email": self.email,
            "role": self.role.value,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
