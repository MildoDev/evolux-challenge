from unittest import TestCase

from flask import url_for

from src import create_app
from src.settings import ConfigTest


class TestFlaskBase(TestCase):
    def setUp(self):
        self.app = create_app(ConfigTest)
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.app.db.create_all()
        self.user = {
            "username": "base",
            "password": "123456",
        }
        self.create_user()

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()

    def create_n_numbers(self, quantity):
        request_data = {
            "value": "",
            "monthyPrice": "0.03",
            "setupPrice": "3.40",
            "currency": "U$",
        }

        response_list = []
        for i in range(quantity):
            request_data["value"] = request_data["value"] + "1"
            response = self.client.post(
                url_for("bp_v1.bp_number.create"),
                json=request_data,
                headers=self.create_token(),
            )
            response_list.append(response.json)

        return response_list

    def create_user(self):
        self.client.post(url_for("bp_v1.bp_user.create"), json=self.user)

    def create_token(self):
        access_token = self.client.post(
            url_for("bp_v1.bp_user.login"), json=self.user
        ).json["access_token"]

        return {"Authorization": f"""Bearer {access_token}"""}
