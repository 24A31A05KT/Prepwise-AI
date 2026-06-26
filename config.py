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

    SQLALCHEMY_TRACK_MODIFICATIONS = Falseimport os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "prepwise_secret_key")

    # Create folders automatically
    DATABASE_DIR = os.path.join(BASE_DIR, "database")
    os.makedirs(DATABASE_DIR, exist_ok=True)

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads", "resumes")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        DATABASE_DIR,
        "app.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False