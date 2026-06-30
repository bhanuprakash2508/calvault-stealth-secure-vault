from flask import (
    Blueprint,
    request,
    jsonify,
    session
)

from models.user import User

hidden_bp = Blueprint(
    "hidden",
    __name__
)

# Verify Secret Pattern

@hidden_bp.route(
    "/verify-pattern",
    methods=["POST"]
)
def verify_pattern():

    data = request.get_json()

    clicked = data.get(
        "sequence"
    )

    user = User.query.first()

    if not user:

        return jsonify(
            {
                "status": "failed"
            }
        )

    if not clicked:

        return jsonify(
            {
                "status": "failed"
            }
        )

    stored_pattern = [
        x.strip()
        for x in user.calendar_pattern.split(",")
    ]

    clicked = [
        str(day)
        for day in clicked
    ]

    if clicked == stored_pattern:

        session["pattern_verified"] = True

        return jsonify(
            {
                "status": "success"
            }
        )

    return jsonify(
        {
            "status": "failed"
        }
    )