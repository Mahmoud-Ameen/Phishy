from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

# app specific
from app.core.exceptions import InvalidCredentials
from app.users.repository import UserRepository


class AuthService:
    @staticmethod
    def login(email: str, password: str) -> str:
        """
        Log the user in by verifying the email and password and generating a jwt token
        :param email: str: the email of the user
        :param password: str: the password of the user
        :return: str: the jwt token
        :raise: InvalidCredentials: if the email or password is incorrect
        """

        # retrieve user object from database
        user = UserRepository.get_by_email(email)
        if not user:
            raise InvalidCredentials("Invalid email or password")

        # check if the password is correct
        if not check_password_hash(user.password_hash, password):
            raise InvalidCredentials("Invalid email or password")

        # generate jwt token
        token = create_access_token(identity=user.email,
                                    additional_claims={"role": user.role, "email": user.email})
        return token
