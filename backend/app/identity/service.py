"""
Service layer for identity operations.
"""
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from .entity import User, UserRole
from .repository import UserRepository
from app.core.exceptions import UserAlreadyExists, InvalidCredentials


class IdentityService:
    """Service for identity operations including user management and authentication."""
    
    @staticmethod
    def register_user(email: str, role: UserRole, first_name: str, last_name: str, password: str) -> User:
        """
        Register a new user with the system.
        
        Args:
            email: User's email address (will be their username)
            role: User's role in the system
            first_name: User's first name
            last_name: User's last name
            password: User's plain text password (will be hashed)
            
        Returns:
            User: The newly created user entity
            
        Raises:
            UserAlreadyExists: If a user with the given email already exists
        """
        # Check if user already exists
        if UserRepository.get_by_email(email):
            raise UserAlreadyExists("User already exists", 400)

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create the user entity object
        user = User(email, role, first_name, last_name, hashed_password)
        
        # Save the user to the database
        user = UserRepository.create(user)

        return user
        
    @staticmethod
    def login(email: str, password: str) -> str:
        """
        Authenticate a user and generate a JWT token.
        
        Args:
            email: User's email address
            password: User's plain text password
            
        Returns:
            str: JWT token for the authenticated user
            
        Raises:
            InvalidCredentials: If the email or password is incorrect
        """
        # Retrieve user object from database
        user = UserRepository.get_by_email(email)
        if not user:
            raise InvalidCredentials("Invalid email or password")

        # Check if the password is correct
        if not check_password_hash(user.password_hash, password):
            raise InvalidCredentials("Invalid email or password")

        # Generate JWT token
        token = create_access_token(
            identity=user.email,
            additional_claims={"role": user.role.value, "email": user.email}
        )
        return token
        
    @staticmethod
    def get_user_by_email(email: str) -> User:
        """
        Get a user by their email address.
        
        Args:
            email: User's email address
            
        Returns:
            User: The user entity if found, None otherwise
        """
        return UserRepository.get_by_email(email)
        
    @staticmethod
    def get_all_users() -> list[User]:
        """
        Get all users in the system.
        
        Returns:
            list[User]: List of all user entities
        """
        return UserRepository.get_all() 