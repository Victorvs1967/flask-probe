import os


app_dir = os.path.abspath(os.path.dirname(__name__))

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A SECRET KEY'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_PASSWORD = 'victorS77'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'victorsmirnov67@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'victorS77'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

class DevelopementConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or 'postgresql://victors:victor77@localhost/flask_db'

class TestingConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or 'postgresql://victors:victor77@localhost/flask_db'

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or 'postgresql://victors:victor77@localhost/flask_db'
