from typing import Any

from sqlalchemy.exc import IntegrityError

from .entity import UserEntity
from .models import UserModel
from ..core.exceptions import UserAlreadyExists
from ..extensions import db


class UserRepository:
    @staticmethod
    def model_to_entity(user_model: UserModel) -> UserEntity:
        print("user role ", user_model.role)
        return UserEntity(
            email=user_model.email,
            role=user_model.role.value,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            password_hash=user_model.password
        )

    @staticmethod
    def entity_to_model(user_entity: UserEntity) -> UserModel:
        user_model = UserModel(
            email=user_entity.email,
            role=user_entity.role.value,
            first_name=user_entity.first_name,
            last_name=user_entity.last_name,
            password=user_entity.password_hash
        )
        return user_model

    @staticmethod
    def create(user: UserEntity) -> UserEntity:

        user_model = UserRepository.entity_to_model(user)

        try:
            db.session.add(user_model)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise UserAlreadyExists("User already exists")

        return user

    @staticmethod
    def get_by_email(email: str) -> UserEntity | None:
        print("ol")
        user_model = UserModel.query.filter_by(email=email).first()

        if not user_model:
            return None

        return UserRepository.model_to_entity(user_model)
