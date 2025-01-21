from decouple import config as decouple_config


class Config:
    SQLALCHEMY_DATABASE_URI = decouple_config("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = decouple_config("SQLALCHEMY_TRACK_MODIFICATIONS")
    JWT_SECRET_KEY = decouple_config("JWT_SECRET_KEY")
    JWT_VERIFY_SUB = False


class ConfigTest(Config):
    SQLALCHEMY_DATABASE_URI = decouple_config(
        "SQLALCHEMY_DATABASE_URI_TEST", default=None
    )
