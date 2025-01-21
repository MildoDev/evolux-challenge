from passlib.hash import pbkdf2_sha256

from src.base.models import BaseModel
from src.extensions import db


class User(BaseModel):
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

    def generate_password_hash(self):
        self.password = pbkdf2_sha256.hash(self.password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)

    def __repr__(self):
        return self._repr(id=self.id, username=self.username)
