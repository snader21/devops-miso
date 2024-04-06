from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.config.config import env_config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(env_config['config'])
    db.init_app(app)
    return app
