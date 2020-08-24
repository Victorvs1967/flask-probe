import os, config
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Command, Shell
from flask_login import LoginManager


db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'


def create_app(config):

    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
