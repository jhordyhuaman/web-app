# services/users/project/config.py

import os


class BaseConfig:
    """Configuración base"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # nuevo
    SECRET_KEY = os.environ.get('SECRET_KEY')  # nuevo
    DEBUG_TB_ENABLED = False              # nuevo
    DEBUG_TB_INTERCEPT_REDIRECTS = False  # nuevo
    BCRYPT_LOG_ROUNDS = 13
    TOKEN_EXPIRATION_DAYS = 30    # nuevo
    TOKEN_EXPIRATION_SECONDS = 0  # nuevo


class DevelopmentConfig(BaseConfig):
    """Configuración de desarrollo"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")  # nuevo
    DEBUG_TB_ENABLED = True  # nuevo
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    """Configuración de Testing"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")  # nuevo
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRATION_DAYS = 0     # nuevo
    TOKEN_EXPIRATION_SECONDS = 3  # nuevo


class ProductionConfig(BaseConfig):
    """Configuración de producción"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")  # nuevo
