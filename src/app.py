import os

from flask_restful import Api

from src import create_app, db
from src.routes.routes import add_resources

app = create_app()
app.app_context().push()
db.create_all()
api = Api(app)
add_resources(api)
