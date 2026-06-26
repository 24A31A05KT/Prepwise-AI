from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.interview import Interview

history = Blueprint("history", __name__)

@history.route("/history")
@login_required
def history_page():

    interviews = (
        Interview.query
        .filter_by(user_id=current_user.id)
        .order_by(Interview.created_at.desc())
        .all()
    )

    return render_template(
        "history.html",
        interviews=interviews
    )