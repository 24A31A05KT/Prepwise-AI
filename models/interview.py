from datetime import datetime
from models.user import db

class Interview(db.Model):

    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    interview_type = db.Column(db.String(50))
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    score = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    ideal_answer = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)