"""
Repository for identity data access.
"""
from typing import Any, Optional
from sqlalchemy.exc import IntegrityError

from .entity import User, UserRole
from .models import UserModel
from app.core.exceptions import UserAlreadyExists
from app.extensions import db


class UserRepository:
    """Repository for user data access operations."""
    
    @staticmethod
    def model_to_entity(user_model: UserModel) -> User:
        """Convert a UserModel to a User entity."""
        return User(
            email=user_model.email,
            role=UserRole(user_model.role.value),
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            password_hash=user_model.password
        )

    @staticmethod
    def entity_to_model(user_entity: User) -> UserModel:
        """Convert a User entity to a UserModel."""
        user_model = UserModel(
            email=user_entity.email,
            role=user_entity.role.value,
            first_name=user_entity.first_name,
            last_name=user_entity.last_name,
            password=user_entity.password_hash
        )
        return user_model

    @staticmethod
    def create(user: User) -> User:
        """Create a new user in the database."""
        print(f"Creating user: {user}")
        user_model = UserRepository.entity_to_model(user)

        try:
            db.session.add(user_model)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise UserAlreadyExists("User already exists")

        return user

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        """Get a user by email address."""
        user_model = UserModel.query.filter_by(email=email).first()

        if not user_model:
            return None

        return UserRepository.model_to_entity(user_model)
        
    @staticmethod
    def get_all() -> list[User]:
        """Get all users from the database."""
        user_models = UserModel.query.all()
        return [UserRepository.model_to_entity(model) for model in user_models]
        
    @staticmethod
    def update(user: User) -> User:
        """Update an existing user in the database."""
        user_model = UserModel.query.get(user.email)
        if not user_model:
            raise ValueError(f"User with email {user.email} not found")
            
        user_model.first_name = user.first_name
        user_model.last_name = user.last_name
        user_model.role = user.role
        # Only update password if it's not empty
        if user.password_hash:
            user_model.password = user.password_hash
            
        db.session.commit()
        return user 