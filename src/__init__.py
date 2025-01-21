from pathlib import Path

from flask import Blueprint, Flask, json, request
from flask_jwt_extended import verify_jwt_in_request
from werkzeug.exceptions import HTTPException

from src.extensions import db, jwt, ma, migrate
from src.modules.number.views import bp_number
from src.modules.user.views import bp_user
from src.settings import Config


def handle_http_exception(e):
    response = e.get_response()
    response.data = json.dumps({"message": e.name, "errors": e.description})
    response.content_type = "application/json"

    return response


def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db, directory=Path(__file__).parent.joinpath("migrations"))
    jwt.init_app(app)

    app.db = db


def register_blueprints(app):
    bp_v1 = Blueprint("bp_v1", __name__)

    bp_v1.register_blueprint(bp_user, url_prefix="/users")
    bp_v1.register_blueprint(bp_number, url_prefix="/numbers")

    app.register_blueprint(bp_v1, url_prefix="/api/v1")


def create_app(config_object=Config):
    app = Flask(__name__)

    app.config.from_object(config_object)

    app.register_error_handler(HTTPException, handle_http_exception)

    register_extensions(app)
    register_blueprints(app)

    @app.before_request
    def verify_jwt():
        if request.endpoint is not None:  # pragma: no cover
            if getattr(app.view_functions[request.endpoint], "is_refresh_token", False):
                verify_jwt_in_request(refresh=True, verify_type=True)
            elif not getattr(app.view_functions[request.endpoint], "is_public", False):
                verify_jwt_in_request(refresh=False, verify_type=True)

    return app
