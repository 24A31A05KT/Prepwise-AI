from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import login_required, current_user

from werkzeug.utils import secure_filename

import os

from models.user import db
from models.resume import Resume

from services.ats_service import analyze_resume

resume = Blueprint("resume", __name__)

ALLOWED_EXTENSIONS = {
    "pdf",
    "doc",
    "docx"
}


def allowed_file(filename):

    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@resume.route("/resume", methods=["GET", "POST"])
@login_required
def resume_page():

    if request.method == "POST":

        if "resume" not in request.files:

            flash("Please choose a resume.", "danger")

            return redirect(request.url)

        file = request.files["resume"]

        if file.filename == "":

            flash("No file selected.", "warning")

            return redirect(request.url)

        if not allowed_file(file.filename):

            flash(
                "Only PDF, DOC and DOCX are allowed.",
                "danger"
            )

            return redirect(request.url)

        filename = secure_filename(file.filename)

        upload_folder = current_app.config["UPLOAD_FOLDER"]

        os.makedirs(upload_folder, exist_ok=True)

        filepath = os.path.join(
            upload_folder,
            filename
        )

        file.save(filepath)

        old_resume = Resume.query.filter_by(
            user_id=current_user.id
        ).first()

        if old_resume:

            old_resume.filename = filename

        else:

            db.session.add(

                Resume(

                    filename=filename,

                    user_id=current_user.id

                )

            )

        db.session.commit()

        flash(
            "Resume uploaded successfully!",
            "success"
        )

        try:

            result = analyze_resume(filepath)

            return render_template(

                "ats_results.html",

                result=result

            )

        except Exception as e:

            print(e)

            flash(
                "ATS Analysis Failed",
                "danger"
            )

            return redirect(
                url_for("resume.resume_page")
            )

    return render_template(
        "resume.html"
    )