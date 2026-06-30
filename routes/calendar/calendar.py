from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    redirect,
    url_for
)

from models.event import Event
from models.user import User
from extensions import db


calendar_bp = Blueprint(
    "calendar",
    __name__
)

# Home Page

@calendar_bp.route("/")
def home():

    user = User.query.first()

    if not user:

        return redirect(
            url_for("setup.setup")
        )

    events = Event.query.all()
    event_list = []

    for event in events:

        color = "#2563eb"

        if event.event_type == "note":
            color = "#059669"

        elif event.event_type == "reminder":
            color = "#d97706"

        elif event.event_type == "deadline":
            color = "#dc2626"

        event_list.append(
            {
                "id": str(event.id),
                "title": event.title,
                "date": event.event_date,
                "color": color,
                "type": event.event_type,
                "description": event.description
            }
        )

    return render_template(
        "calendar/calendar.html",
        events=event_list
    )

# Add Event

@calendar_bp.route(
    "/add-event",
    methods=["POST"]
)
def add_event():

    data = request.get_json()

    event = Event(
        title=data.get("title"),
        event_date=data.get("date"),
        event_type=data.get("type"),
        description=data.get("description")
    )

    db.session.add(event)
    db.session.commit()

    return jsonify(
        {
            "status": "success"
        }
    )

# Update Event

@calendar_bp.route(
    "/update-event/<int:event_id>",
    methods=["POST"]
)
def update_event(event_id):

    data = request.get_json()

    event = Event.query.get(
        event_id
    )

    if not event:

        return jsonify(
            {
                "status": "error"
            }
        )

    event.title = data.get("title")
    event.event_date = data.get("date")
    event.event_type = data.get("type")
    event.description = data.get("description")

    db.session.commit()

    return jsonify(
        {
            "status": "success"
        }
    )

# Delete Event

@calendar_bp.route(
    "/delete-event/<int:event_id>",
    methods=["POST"]
)
def delete_event(event_id):

    event = Event.query.get(
        event_id
    )

    if not event:

        return jsonify(
            {
                "status": "error"
            }
        )

    db.session.delete(event)
    db.session.commit()

    return jsonify(
        {
            "status": "success"
        }
    )