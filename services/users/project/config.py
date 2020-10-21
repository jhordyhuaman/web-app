# services/users/project/config.py


import os  # new


class BaseConfig:
    """Configuracion Base"""

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "my_key"  # nuevo


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")  # new


class TestingConfig(BaseConfig):
    """Configuracion de Testing"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")  # nuevo


class ProductionConfig(BaseConfig):
    """Configuracion de Production"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")  # nuevo
