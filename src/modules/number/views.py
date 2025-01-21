from flask import Blueprint, abort, current_app, request, url_for
from marshmallow import ValidationError

from src.modules.number.models import Number
from src.modules.number.serializers import NumberSchema

bp_number = Blueprint("bp_number", __name__)


@bp_number.route("/list", methods=["GET"])
def list():
    page = request.args.get("page", type=int)
    per_page = request.args.get("per_page", type=int)

    numbers = Number.query.paginate(page=page, per_page=per_page)

    next_url = (
        url_for(
            "bp_v1.bp_number.list", page=numbers.page + 1, per_page=numbers.per_page
        )
        if numbers.has_next
        else None
    )
    previous_url = (
        url_for(
            "bp_v1.bp_number.list", page=numbers.page - 1, per_page=numbers.per_page
        )
        if numbers.has_prev
        else None
    )

    return {
        "results": NumberSchema(many=True).dump(numbers.items),
        "pagination": {
            "count": numbers.total,
            "page": numbers.page,
            "per_page": numbers.per_page,
            "pages": numbers.pages,
            "next": next_url,
            "previous": previous_url,
        },
    }, 200


@bp_number.route("/<int:id>", methods=["GET"])
def show(id):
    number = current_app.db.session.get(Number, id)

    if number is None:
        abort(404)

    return NumberSchema().jsonify(number), 200


@bp_number.route("/create", methods=["POST"])
def create():
    try:
        number = NumberSchema().load(request.json)
        if Number.query.filter_by(value=number.value).first() is not None:
            raise ValidationError({"value": ["Value already exists."]})
    except ValidationError as e:
        return {"message": "ValidationError", "errors": e.messages}, 422

    current_app.db.session.add(number)
    current_app.db.session.commit()

    return NumberSchema().jsonify(number), 201


@bp_number.route("<int:id>/update", methods=["PATCH"])
def update(id):
    validation_errors = NumberSchema(partial=True).validate(request.json)
    if validation_errors:
        return {"message": "ValidationError", "errors": validation_errors}, 422

    number = Number.query.filter_by(id=id)

    if number.first() is None:
        abort(404)

    number.update(request.json)
    current_app.db.session.commit()

    return NumberSchema().jsonify(number.first()), 200


@bp_number.route("<int:id>/delete", methods=["DELETE"])
def delete(id):
    number = current_app.db.session.get(Number, id)

    if number is None:
        abort(404)

    current_app.db.session.delete(number)
    current_app.db.session.commit()

    return {}, 204
