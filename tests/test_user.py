from flask import url_for
from test_flask_base import TestFlaskBase

from src.modules.user.models import User


class TestUserCreate(TestFlaskBase):
    def test_create_success(self):
        request_data = {
            "username": "test",
            "password": "123456",
        }

        response = self.client.post(url_for("bp_v1.bp_user.create"), json=request_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["username"], request_data["username"])

    def test_create_missing_field_failure(self):
        request_data = {"username": "test"}

        expected_response = {
            "message": "ValidationError",
            "errors": {"password": ["Missing data for required field."]},
        }

        response = self.client.post(url_for("bp_v1.bp_user.create"), json=request_data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)

    def test_create_blank_field_failure(self):
        request_data = {
            "username": "",
            "password": "123456",
        }

        expected_response = {
            "message": "ValidationError",
            "errors": {"username": "Field is blank."},
        }

        response = self.client.post(url_for("bp_v1.bp_user.create"), json=request_data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)

    def test_create_empty_failure(self):
        request_data = {}

        expected_response = {
            "message": "ValidationError",
            "errors": {
                "username": ["Missing data for required field."],
                "password": ["Missing data for required field."],
            },
        }

        response = self.client.post(url_for("bp_v1.bp_user.create"), json=request_data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)

    def test_create_id_unknown_field_failure(self):
        request_data = {
            "id": 1,
            "username": "test",
            "password": "123456",
        }

        expected_response = {
            "message": "ValidationError",
            "errors": {"id": ["Unknown field."]},
        }

        response = self.client.post(url_for("bp_v1.bp_user.create"), json=request_data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)

    def test_create_non_unique_username_failure(self):
        request_data = {
            "username": "test",
            "password": "123456",
        }

        expected_response = {
            "message": "ValidationError",
            "errors": {"username": ["Username already exists."]},
        }

        self.client.post(url_for("bp_v1.bp_user.create"), json=request_data)
        response = self.client.post(url_for("bp_v1.bp_user.create"), json=request_data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)


class TestUserLogin(TestFlaskBase):
    def test_login_success(self):
        response = self.client.post(url_for("bp_v1.bp_user.login"), json=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.json.keys()), ["access_token", "refresh_token"])

    def test_login_invalid_credentials(self):
        request_data = {
            "username": "invalid",
            "password": "123456",
        }

        expected_response = {
            "message": "AuthenticationError",
            "errors": {"_credentials": ["Invalid credentials."]},
        }

        response = self.client.post(url_for("bp_v1.bp_user.login"), json=request_data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, expected_response)

    def test_login_missing_field_failure(self):
        request_data = {
            "password": "123456",
        }

        expected_response = {
            "message": "ValidationError",
            "errors": {"username": ["Missing data for required field."]},
        }

        response = self.client.post(url_for("bp_v1.bp_user.login"), json=request_data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)

    def test_login_blank_field_failure(self):
        request_data = {
            "username": "",
            "password": "123456",
        }

        expected_response = {
            "message": "ValidationError",
            "errors": {"username": "Field is blank."},
        }

        response = self.client.post(url_for("bp_v1.bp_user.login"), json=request_data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)

    def test_login_empty_failure(self):
        request_data = {}

        expected_response = {
            "message": "ValidationError",
            "errors": {
                "username": ["Missing data for required field."],
                "password": ["Missing data for required field."],
            },
        }

        response = self.client.post(url_for("bp_v1.bp_user.login"), json=request_data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)

    def test_login_id_unknown_field_failure(self):
        request_data = {
            "id": 1,
            "username": "test",
            "password": "123456",
        }

        expected_response = {
            "message": "ValidationError",
            "errors": {"id": ["Unknown field."]},
        }

        response = self.client.post(url_for("bp_v1.bp_user.login"), json=request_data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)


class TestUserAccessToken(TestFlaskBase):
    def test_access_token_success(self):
        access_token = self.client.post(
            url_for("bp_v1.bp_user.login"), json=self.user
        ).json["access_token"]

        response = self.client.get(
            url_for("bp_v1.bp_number.list"),
            headers={"Authorization": f"""Bearer {access_token}"""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["results"], [])

    def test_access_token_missing_authorization_header_failure(self):
        expected_response = {"msg": "Missing Authorization Header"}

        response = self.client.get(url_for("bp_v1.bp_number.list"))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, expected_response)

    def test_access_token_blank_authorization_header_failure(self):
        expected_response = {
            "msg": "Bad Authorization header. Expected 'Authorization: Bearer <JWT>'"
        }

        response = self.client.get(
            url_for("bp_v1.bp_number.list"), headers={"Authorization": "Bearer "}
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)

    def test_access_token_using_refresh_token_failure(self):
        expected_response = {"msg": "Only non-refresh tokens are allowed"}

        refresh_token = self.client.post(
            url_for("bp_v1.bp_user.login"), json=self.user
        ).json["refresh_token"]

        response = self.client.get(
            url_for("bp_v1.bp_number.list"),
            headers={"Authorization": f"""Bearer {refresh_token}"""},
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)


class TestUserRefreshToken(TestFlaskBase):
    def test_refresh_token_success(self):
        refresh_token = self.client.post(
            url_for("bp_v1.bp_user.login"), json=self.user
        ).json["refresh_token"]

        response = self.client.post(
            url_for("bp_v1.bp_user.refresh_token"),
            headers={"Authorization": f"""Bearer {refresh_token}"""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.json.keys()), ["access_token"])

    def test_refresh_token_missing_authorization_header_failure(self):
        expected_response = {"msg": "Missing Authorization Header"}

        response = self.client.post(url_for("bp_v1.bp_user.refresh_token"))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, expected_response)

    def test_refresh_token_blank_authorization_header_failure(self):
        expected_response = {
            "msg": "Bad Authorization header. Expected 'Authorization: Bearer <JWT>'"
        }

        response = self.client.post(
            url_for("bp_v1.bp_user.refresh_token"), headers={"Authorization": "Bearer "}
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)

    def test_refresh_token_using_access_token_failure(self):
        expected_response = {"msg": "Only refresh tokens are allowed"}

        access_token = self.client.post(
            url_for("bp_v1.bp_user.login"), json=self.user
        ).json["access_token"]

        response = self.client.post(
            url_for("bp_v1.bp_user.refresh_token"),
            headers={"Authorization": f"""Bearer {access_token}"""},
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)


class TestUserModel(TestFlaskBase):
    def test_repr_blank_success(self):
        user_repr = repr(User())

        self.assertEqual(
            user_repr,
            """<User (id=None, username=None)>""",
        )

    def test_repr_non_blank_success(self):
        user_repr = repr(User(id=1, username="test"))

        self.assertEqual(
            user_repr,
            """<User (id=1, username=test)>""",
        )
