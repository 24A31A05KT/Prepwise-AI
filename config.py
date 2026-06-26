import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads", "resumes")

    SECRET_KEY = "prepwise_secret_key"

    SQLALCHEMY_DATABASE_URI = \
        "sqlite:///" + os.path.join(
            BASE_DIR,
            "database",
            "app.db"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False