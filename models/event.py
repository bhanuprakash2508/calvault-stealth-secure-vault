from datetime import datetime
from extensions import db


class Event(db.Model):

    __tablename__ = "events"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    event_date = db.Column(
        db.String(20),
        nullable=False
    )

    event_type = db.Column(
        db.String(30),
        default="event"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )