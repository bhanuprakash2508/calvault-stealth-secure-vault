import os

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

class Config:

    # Flask Session Secret Key

    SECRET_KEY = os.getenv(

        "SECRET_KEY",
        "fallback-secret-key"
    )

    # SQLite Database

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(

        BASE_DIR,
        "instance",
        "calvault.db"
    )

    # Disable unnecessary tracking

    SQLALCHEMY_TRACK_MODIFICATIONS = False