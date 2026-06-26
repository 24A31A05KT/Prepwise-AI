from flask import Blueprint, render_template
from flask_login import login_required

results = Blueprint("results", __name__)

@results.route("/results")
@login_required
def results_page():
    return render_template("results.html")