import uuid
import json
from unittest import TestCase
from unittest.mock import patch
import datetime

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
        self.token = "my-secret-key"

    def tearDown(self):
        pass

    # def test_ping(self):

        # Define endpoint and headers
        endpoint = "/blacklists/ping"

        # Make a request to endpoint
        res = self.client.get(endpoint)

        # Assert that the response status code is 200
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            res.get_json(), "pong")

    @patch('src.infrastructure.dao.DAO.find_one_by_options')
    @patch('src.infrastructure.dao.DAO.create')
    def test_add_to_blacklist(self, mock_create, mock_find_one_by_options):

        # Define endpoint and headers
        endpoint = "/blacklists"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        # Generate random data
        email = self.data_factory.email()
        app_uuid = str(uuid.uuid4())
        blocked_reason = self.data_factory.sentence()

        mock_create.return_value = {
            "id": str(uuid.uuid4()),
            "ip_address": self.data_factory.ipv4(),
            "email": email,
            "app_uuid": app_uuid,
            "blocked_reason": blocked_reason,
            "created_at": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }

        mock_find_one_by_options.return_value = None

        # Make a request to endpoint
        res = self.client.post(endpoint, headers=headers, data=json.dumps({
            "email": email,
            "app_uuid": app_uuid,
            "blocked_reason": blocked_reason
        }))

        # Assert that the response status code is 201
        self.assertEqual(res.status_code, 201)

        email_res = res.get_json()["data"]["email"]
        app_uuid_res = res.get_json()["data"]["app_uuid"]
        blocked_at_res = res.get_json()["data"]["blocked_reason"]

        self.assertEqual(email_res, email)
        self.assertEqual(app_uuid_res, app_uuid)
        self.assertEqual(blocked_at_res, blocked_reason)

    def test_add_to_blacklist_missing_email(self):

        # Define endpoint and headers
        endpoint = "/blacklists"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        # Make a request to endpoint
        res = self.client.post(endpoint, headers=headers, data=json.dumps({
            "app_uuid": str(uuid.uuid4()),
            "blocked_reason": self.data_factory.sentence()
        }))

        # Assert that the response status code is 400
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json().get('msg'), "Campo email es requerido")

    @patch('src.infrastructure.dao.DAO.find_one_by_options')
    def test_get_email_in_blacklist(self, mock_find_one_by_options):

        email = self.data_factory.email()

        mock_find_one_by_options.return_value = {
            "id": str(uuid.uuid4()),
            "ip_address": self.data_factory.ipv4(),
            "email": email,
            "app_uuid": str(uuid.uuid4()),
            "blocked_reason": self.data_factory.sentence(),
            "created_at": datetime.datetime.utcnow()
        }

        # Define endpoint and headers
        endpoint = f"/blacklists/{email}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        # Make a request to endpoint
        res = self.client.get(endpoint, headers=headers)

        # Assert that the response status code is 200
        self.assertEqual(res.status_code, 200)

        email_res = res.get_json().get("data")
        self.assertTrue(email_res.get("encontrado"))
        self.assertEqual(email_res.get(
            "blocked_reason"), mock_find_one_by_options.return_value.get("blocked_reason"))

    @patch('src.infrastructure.dao.DAO.find_one_by_options')
    def test_get_email_not_in_blacklist(self, mock_find_one_by_options):

        email = self.data_factory.email()

        mock_find_one_by_options.return_value = None

        # Define endpoint and headers
        endpoint = f"/blacklists/{email}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        # Make a request to endpoint
        res = self.client.get(endpoint, headers=headers)

        # Assert that the response status code is 404
        self.assertEqual(res.status_code, 404)

        email_res = res.get_json().get("data")
        self.assertFalse(email_res.get("encontrado"))
