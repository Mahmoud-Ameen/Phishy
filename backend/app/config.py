import os

from dotenv import load_dotenv


class Config:
    load_dotenv()
    
    # Flask Related
    SERVER_PORT = os.environ.get('SERVER_PORT', 3000)
    SERVER_HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    DEBUG = True

    # DB Related
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///database.db')

    # JWT Related
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "Mahmoud")
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24 * 3 # 3 days

    # Tracking Related
    TRACKING_URL = os.environ.get('TRACKING_URL', 'http://localhost:5000/api/tracking/open')
