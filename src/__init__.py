from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.config.config import env_config

db = SQLAlchemy()


def create_app(app_env):
    app = Flask(__name__)
    app.app_context().push()
    if app_env == 'dev' or app_env == 'prod':
        app.config.from_object(env_config['config'])
        db.init_app(app)
        db.create_all()
    return app
