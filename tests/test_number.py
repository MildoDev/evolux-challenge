from flask import url_for
from test_flask_base import TestFlaskBase

from src.modules.number.models import Number

not_found_response = {
    "errors": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
    "message": "Not Found",
}


class TestNumberList(TestFlaskBase):
    def test_list_empty_success(self):
        response = self.client.get(
            url_for("bp_v1.bp_number.list"), headers=self.create_token()
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["pagination"]["count"], 0)
        self.assertEqual(response.json["results"], [])

    def test_list_one_success(self):
        create_numbers_response_list = self.create_n_numbers(1)

        response = self.client.get(
            url_for("bp_v1.bp_number.list"), headers=self.create_token()
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["pagination"]["count"], 1)
        self.assertEqual(response.json["results"], create_numbers_response_list)

    def test_list_n_success(self):
        create_numbers_response_list = self.create_n_numbers(15)

        response = self.client.get(
            url_for("bp_v1.bp_number.list"), headers=self.create_token()
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["pagination"]["count"], 15)
        self.assertEqual(response.json["results"], create_numbers_response_list)

    def test_list_pagination_success(self):
        create_numbers_response_list = self.create_n_numbers(30)
        page = 3
        per_page = 5

        response = self.client.get(
            url_for("bp_v1.bp_number.list", page=page, per_page=per_page),
            headers=self.create_token(),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["pagination"]["count"], 30)
        self.assertEqual(response.json["pagination"]["page"], page)
        self.assertEqual(response.json["pagination"]["per_page"], per_page)
        self.assertEqual(
            response.json["results"],
            create_numbers_response_list[(page - 1) * per_page : page * per_page],
        )

    def test_list_pagination_implicit_page_success(self):
        create_numbers_response_list = self.create_n_numbers(30)
        per_page = 5

        response = self.client.get(
            url_for("bp_v1.bp_number.list", per_page=per_page),
            headers=self.create_token(),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["pagination"]["count"], 30)
        self.assertEqual(response.json["pagination"]["page"], 1)
        self.assertEqual(response.json["pagination"]["per_page"], per_page)
        self.assertEqual(
            response.json["results"], create_numbers_response_list[:per_page]
        )

    def test_list_pagination_implicit_per_page_success(self):
        create_numbers_response_list = self.create_n_numbers(30)
        page = 1

        response = self.client.get(
            url_for("bp_v1.bp_number.list", page=page),
            headers=self.create_token(),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["pagination"]["count"], 30)
        self.assertEqual(response.json["pagination"]["page"], page)
        self.assertEqual(response.json["pagination"]["per_page"], 20)
        self.assertEqual(
            response.json["results"],
            create_numbers_response_list[(page - 1) * 20 : page * 20],
        )

    def test_list_pagination_invalid_page_failure(self):
        self.create_n_numbers(30)
        page = -1
        per_page = 5

        response = self.client.get(
            url_for("bp_v1.bp_number.list", page=page, per_page=per_page),
            headers=self.create_token(),
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, not_found_response)

    def test_list_pagination_invalid_per_page_failure(self):
        self.create_n_numbers(30)
        page = 1
        per_page = -1

        response = self.client.get(
            url_for("bp_v1.bp_number.list", page=page, per_page=per_page),
            headers=self.create_token(),
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, not_found_response)

    def test_list_pagination_invalid_page_and_per_page_failure(self):
        self.create_n_numbers(30)
        page = -1
        per_page = -1

        response = self.client.get(
            url_for("bp_v1.bp_number.list", page=page, per_page=per_page),
            headers=self.create_token(),
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, not_found_response)


class TestNumberShow(TestFlaskBase):
    def test_show_success(self):
        create_numbers_response_list = self.create_n_numbers(1)

        response = self.client.get(
            url_for("bp_v1.bp_number.show", id=1), headers=self.create_token()
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, create_numbers_response_list[0])

    def test_show_invalid_id_failure(self):

        response = self.client.get(
            url_for("bp_v1.bp_number.show", id=1), headers=self.create_token()
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, not_found_response)


class TestNumberCreate(TestFlaskBase):
    def test_create_success(self):
        request_data = {
            "value": "+55 84 91234-4321",
            "monthyPrice": "0.03",
            "setupPrice": "3.40",
            "currency": "U$",
        }

        response = self.client.post(
            url_for("bp_v1.bp_number.create"),
            json=request_data,
            headers=self.create_token(),
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, request_data | {"id": 1})

    def test_create_missing_field_failure(self):
        request_data = {
            "monthyPrice": "0.03",
            "setupPrice": "3.40",
            "currency": "U$",
        }

        expected_response = {
            "message": "ValidationError",
            "errors": {"value": ["Missing data for required field."]},
        }

        response = self.client.post(
            url_for("bp_v1.bp_number.create"),
            json=request_data,
            headers=self.create_token(),
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)

    def test_create_blank_field_failure(self):
        request_data = {
            "value": "",
            "monthyPrice": "0.03",
            "setupPrice": "3.40",
            "currency": "U$",
        }

        expected_response = {
            "message": "ValidationError",
            "errors": {"value": "Field is blank."},
        }

        response = self.client.post(
            url_for("bp_v1.bp_number.create"),
            json=request_data,
            headers=self.create_token(),
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)

    def test_create_empty_failure(self):
        request_data = {}

        expected_response = {
            "message": "ValidationError",
            "errors": {
                "value": ["Missing data for required field."],
                "monthyPrice": ["Missing data for required field."],
                "currency": ["Missing data for required field."],
                "setupPrice": ["Missing data for required field."],
            },
        }

        response = self.client.post(
            url_for("bp_v1.bp_number.create"),
            json=request_data,
            headers=self.create_token(),
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)

    def test_create_id_unknown_field_failure(self):
        request_data = {
            "id": 1,
            "value": "+55 84 91234-4321",
            "monthyPrice": "0.03",
            "setupPrice": "3.40",
            "currency": "U$",
        }

        expected_response = {
            "message": "ValidationError",
            "errors": {"id": ["Unknown field."]},
        }

        response = self.client.post(
            url_for("bp_v1.bp_number.create"),
            json=request_data,
            headers=self.create_token(),
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)

    def test_create_non_unique_value_failure(self):
        request_data = {
            "value": "+55 84 91234-4321",
            "monthyPrice": "0.03",
            "setupPrice": "3.40",
            "currency": "U$",
        }

        expected_response = {
            "message": "ValidationError",
            "errors": {"value": ["Value already exists."]},
        }

        self.client.post(
            url_for("bp_v1.bp_number.create"),
            json=request_data,
            headers=self.create_token(),
        )
        response = self.client.post(
            url_for("bp_v1.bp_number.create"),
            json=request_data,
            headers=self.create_token(),
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)


class TestNumberUpdate(TestFlaskBase):
    def test_update_success(self):
        create_numbers_response_list = self.create_n_numbers(1)

        change_data = {"currency": "BRL"}

        expected_response = create_numbers_response_list[0] | change_data

        response = self.client.patch(
            url_for("bp_v1.bp_number.update", id=1),
            json=change_data,
            headers=self.create_token(),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_response)

    def test_update_blank_field_failure(self):
        self.create_n_numbers(1)

        change_data = {"value": ""}

        expected_response = {
            "message": "ValidationError",
            "errors": {"value": "Field is blank."},
        }

        response = self.client.patch(
            url_for("bp_v1.bp_number.update", id=1),
            json=change_data,
            headers=self.create_token(),
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)

    def test_update_empty_failure(self):
        self.create_n_numbers(1)

        change_data = {}

        expected_response = {
            "message": "ValidationError",
            "errors": {"_schema": ["Content is empty."]},
        }

        response = self.client.patch(
            url_for("bp_v1.bp_number.update", id=1),
            json=change_data,
            headers=self.create_token(),
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)

    def test_update_id_unknown_field_failure(self):
        self.create_n_numbers(1)

        change_data = {"id": 1}

        expected_response = {
            "message": "ValidationError",
            "errors": {"id": ["Unknown field."]},
        }

        response = self.client.patch(
            url_for("bp_v1.bp_number.update", id=1),
            json=change_data,
            headers=self.create_token(),
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, expected_response)

    def test_update_invalid_id_failure(self):
        change_data = {"currency": "BRL"}

        response = self.client.patch(
            url_for("bp_v1.bp_number.update", id=1),
            json=change_data,
            headers=self.create_token(),
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, not_found_response)


class TestNumberDelete(TestFlaskBase):
    def test_delete_success(self):
        self.create_n_numbers(1)

        response = self.client.delete(
            url_for("bp_v1.bp_number.delete", id=1), headers=self.create_token()
        )

        self.assertEqual(response.status_code, 204)

    def test_delete_invalid_id_failure(self):

        response = self.client.delete(
            url_for("bp_v1.bp_number.delete", id=1), headers=self.create_token()
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, not_found_response)


class TestNumberModel(TestFlaskBase):
    def test_repr_blank_success(self):
        number_repr = repr(Number())

        self.assertEqual(
            number_repr,
            """<Number (id=None, value=None, monthyPrice=None, setupPrice=None, currency=None)>""",
        )

    def test_repr_non_blank_success(self):
        number_repr = repr(
            Number(
                id=42,
                value="+55 84 91234-4321",
                monthyPrice="0.03",
                setupPrice="3.40",
                currency="U$",
            )
        )

        self.assertEqual(
            number_repr,
            """<Number (id=42, value=+55 84 91234-4321, monthyPrice=0.03, setupPrice=3.40, currency=U$)>""",
        )
