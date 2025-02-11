import os


class Config:

    # Flask Related
    SERVER_PORT = os.environ.get('SERVER_PORT', 3000)
    SERVER_HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    DEBUG = True

    # DB Related
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///database.db')

    # JWT Related
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "Mahmoud")
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24  # 1 day
