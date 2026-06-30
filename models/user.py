from datetime import datetime
from extensions import db

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    vault_password = db.Column(
        db.String(255),
        nullable=False
    )

    calendar_pattern = db.Column(
        db.String(50),
        nullable=False
    )

    setup_completed = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    recovery_key = db.Column(

        db.String(100),
        nullable=True
    )