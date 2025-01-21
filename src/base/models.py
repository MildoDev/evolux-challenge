from src.extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def _repr(self, **fields):
        model_name = self.__class__.__name__
        fields_string = ", ".join(
            [f"""{field}={value}""" for field, value in fields.items()]
        )

        return f"""<{model_name} ({fields_string})>"""
