from werkzeug.security import generate_password_hash

# app specific
from .entity import UserEntity, UserRole
from .repository import UserRepository
from ..core.exceptions import UserAlreadyExists


class UserService:

    @staticmethod
    def register_user(email: str, role: UserRole, first_name: str, last_name: str, password: str) -> UserEntity:
        # check if user already exists
        if UserRepository.get_by_email(email):
            raise UserAlreadyExists("User already exists", 400)

        # hash the password
        hashed_password = generate_password_hash(password)

        # create the user entity object
        user = UserEntity(email, role, first_name, last_name, hashed_password)
        # save the user to the database
        user = UserRepository.create(user)

        return user

