from flask import Flask, render_template
from flask_login import LoginManager

from config import Config
from models.user import db, User
from models.interview import Interview

# Blueprints
from routes.auth import auth
from routes.dashboard import dashboard
from routes.resume import resume
from routes.interview import interview
from routes.profile import profile
from routes.history import history
from routes.results import results


app = Flask(__name__)
app.config.from_object(Config)

# ---------------- Database ---------------- #

db.init_app(app)

# ---------------- Login Manager ---------------- #

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------- Home ---------------- #

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- Register Blueprints ---------------- #

app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(resume)
app.register_blueprint(interview)
app.register_blueprint(profile)
app.register_blueprint(history)
app.register_blueprint(results)

import os

os.makedirs("database", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("uploads/resumes", exist_ok=True)
# ---------------- Create Database ---------------- #

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)