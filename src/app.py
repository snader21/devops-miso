import os

from flask_restful import Api


from src import create_app
from src.routes.routes import add_resources

app = create_app("dev")
api = Api(app)
add_resources(api)
