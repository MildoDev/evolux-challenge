from marshmallow import ValidationError, fields, validates_schema

from src.extensions import ma


class BaseSQLAlchemySchema(ma.SQLAlchemySchema):
    class Meta:
        load_instance = True

    id = fields.Int(dump_only=True)

    @validates_schema(skip_on_field_errors=True)
    def content_empty_validation(self, data, **kwargs):
        if data == {}:
            raise ValidationError("Content is empty.")

    @validates_schema(skip_on_field_errors=False)
    def blank_field_validation(self, data, **kwargs):
        errors = {}
        for key in data:
            if data[key] == "":
                errors[key] = "Field is blank."
        if errors:
            raise ValidationError(errors)
