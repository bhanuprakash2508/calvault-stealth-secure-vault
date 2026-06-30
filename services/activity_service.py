from models.activity import ActivityLog
from extensions import db


def log_activity(action):

    try:

        activity = ActivityLog(
            action=action
        )

        db.session.add(
            activity
        )

        db.session.commit()

    except Exception:

        db.session.rollback()