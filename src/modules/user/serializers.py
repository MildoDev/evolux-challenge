from marshmallow import fields

from src.base.serializers import BaseSQLAlchemySchema
from src.modules.user.models import User


class UserSchema(BaseSQLAlchemySchema):
    class Meta(BaseSQLAlchemySchema.Meta):
        model = User

    username = fields.Str(required=True)
    password = fields.Str(required=True)
