import uuid
import json
from unittest import TestCase
from unittest.mock import patch
import random

from faker import Faker
from flask_restful import Api

from src.models.blacklist_model import Blacklist, BlacklistSchema
from src import create_app
from src.routes.routes import add_resources

blackList_schema = BlacklistSchema()


class BlacklistTest(TestCase):
    def setUp(self):
        self.data_factory = Faker()
        self.app = create_app("test")
        self.api = Api(self.app)
        add_resources(self.api)
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_ping(self):

        # Define endpoint and headers
        endpoint = "/blacklists/ping"

        # Make a request to endpoint
        res = self.client.get(endpoint)

        # Assert that the response status code is 200
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            res.get_json(), "pong")
