from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models.resume import Resume
from models.interview import Interview

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/dashboard")
@login_required
def dashboard_page():

    interviews = Interview.query.filter_by(
        user_id=current_user.id
    ).all()

    total_interviews = len(interviews)

    resume = Resume.query.filter_by(
        user_id=current_user.id
    ).first()

    if interviews:

        scores = [i.score for i in interviews]

        average_score = round(sum(scores) / len(scores), 1)

        best_score = max(scores)

        recent_interviews = Interview.query.filter_by(
            user_id=current_user.id
        ).order_by(
            Interview.created_at.desc()
        ).limit(5).all()

    else:

        average_score = 0

        best_score = 0

        recent_interviews = []

    return render_template(

        "dashboard.html",

        user=current_user,

        average_score=average_score,

        best_score=best_score,

        total_interviews=total_interviews,

        resume_uploaded=resume is not None,

        recent_interviews=recent_interviews

    )