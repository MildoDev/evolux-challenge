from flask import Blueprint, current_app, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from marshmallow import ValidationError

from src.base.views import public_endpoint, refresh_token_endpoint
from src.modules.user.models import User
from src.modules.user.serializers import UserSchema

bp_user = Blueprint("bp_user", __name__)


@bp_user.route("/create", methods=["POST"])
@public_endpoint
def create():
    try:
        user = UserSchema().load(request.json)
        if User.query.filter_by(username=user.username).first() is not None:
            raise ValidationError({"username": ["Username already exists."]})
    except ValidationError as e:
        return {"message": "ValidationError", "errors": e.messages}, 422

    user.generate_password_hash()

    current_app.db.session.add(user)
    current_app.db.session.commit()

    return UserSchema().jsonify(user), 201


@bp_user.route("/login", methods=["POST"])
@public_endpoint
def login():
    validation_errors = UserSchema().validate(request.json)
    if validation_errors:
        return {"message": "ValidationError", "errors": validation_errors}, 422

    user = User.query.filter_by(username=request.json["username"]).first()

    if user is not None and user.check_password(request.json["password"]):
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        return {"access_token": access_token, "refresh_token": refresh_token}, 200
    else:
        return {
            "message": "AuthenticationError",
            "errors": {"_credentials": ["Invalid credentials."]},
        }, 401


@bp_user.route("/refresh_token", methods=["POST"])
@refresh_token_endpoint
def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity)

    return {"access_token": access_token}, 200
