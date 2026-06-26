from models.user import db

class History(db.Model):

    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    interview_type = db.Column(db.String(50))

    score = db.Column(db.Integer)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )