import json
import os

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from services.gemini_service import evaluate_interview
from services.gemini_service import ask_gemini
from flask_login import current_user
from models.interview import Interview
from models.user import db

interview = Blueprint("interview", __name__)

# ---------------- Paths ---------------- #

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

QUESTION_FILE = os.path.join(
    BASE_DIR,
    "data",
    "questions.json"
)

# ---------------- AI Selection ---------------- #

@interview.route("/ai-select")
@login_required
def ai_select():
    return render_template("ai_select.html")


# ---------------- Interview Page ---------------- #

@interview.route("/interview")
@login_required
def interview_page():

    interview_type = request.args.get(
        "type",
        "technical"
    )

    if not os.path.exists(QUESTION_FILE):
        return "questions.json not found!", 404

    with open(QUESTION_FILE, "r", encoding="utf-8") as file:
        questions = json.load(file)

    selected_questions = questions.get(
        interview_type,
        questions.get("technical", [])
    )

    print("Interview Type :", interview_type)
    print("Questions :", selected_questions)

    return render_template(
        "interview.html",
        questions=selected_questions,
        interview_type=interview_type
    )
@interview.route("/evaluate-interview", methods=["POST"])
@login_required
def evaluate_all():

    try:

        data = request.get_json()

        questions = data.get("questions", [])

        answers = data.get("answers", [])

        result = evaluate_interview(
            questions,
            answers
        )

        return jsonify(result)

    except Exception as e:

        print(e)

        return jsonify([]), 500
    
@interview.route("/save-interview", methods=["POST"])
@login_required
def save_interview():

    data = request.get_json()
    print(data)
    questions = data.get("questions", [])
    answers = data.get("answers", [])
    feedback = data.get("feedback", [])
    interview_type = data.get("interview_type", "technical")

    try:

        for i in range(len(questions)):

            interview = Interview(

                user_id=current_user.id,

                interview_type=interview_type,

                question=questions[i],

                answer=answers[i] if i < len(answers) else "",

                score=int(feedback[i]["score"]) if i < len(feedback) else 0,

                feedback=feedback[i]["feedback"] if i < len(feedback) else "",

                ideal_answer=feedback[i]["ideal_answer"] if i < len(feedback) else ""

            )

            db.session.add(interview)

        db.session.commit()

        return jsonify({
            "success": True
        })

    except Exception as e:

        db.session.rollback()

        print(e)

        return jsonify({
            "success": False
        })


# ---------------- API: Get Questions ---------------- #

@interview.route("/get-questions")
@login_required
def get_questions():

    interview_type = request.args.get(
        "type",
        "technical"
    )

    with open(QUESTION_FILE, "r", encoding="utf-8") as file:
        questions = json.load(file)

    return jsonify(
        questions.get(
            interview_type,
            questions.get("technical", [])
        )
    )


# ---------------- Gemini Test ---------------- #

@interview.route("/test-gemini")
@login_required
def test_gemini():

    answer = ask_gemini(
        "Generate one Java interview question."
    )

    return jsonify({
        "question": answer
    })