from extensions import db

from datetime import (datetime, timedelta)

class ActivityLog( db.Model ):

    id = db.Column(

        db.Integer,
        primary_key=True
    )

    action = db.Column(

        db.String(200),
        nullable=False
    )

    timestamp = db.Column(

        db.DateTime,
        default=lambda:

            datetime.utcnow()

            + timedelta(
                hours=5,
                minutes=30
            )
    )