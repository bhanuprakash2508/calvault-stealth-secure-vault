from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from models.user import User
from werkzeug.security import generate_password_hash
from extensions import db

recovery_bp = Blueprint(
    "recovery",
    __name__
)


@recovery_bp.route(
    "/recover-access",
    methods=["GET", "POST"]
)
def recover_access():

    user = User.query.first()

    error = None

    if not user:

        return redirect(
            url_for("setup.setup")
        )

    if request.method == "POST":

        entered_key = request.form.get(
            "recovery_key"
        )

        if entered_key == user.recovery_key:

            return redirect(
                url_for("recovery.reset_access")
            )

        else:

            error = "Invalid Recovery Key"

    return render_template(
        "auth/recover_access.html",
        error=error
    )


@recovery_bp.route(
    "/reset-access",
    methods=["GET", "POST"]
)
def reset_access():

    user = User.query.first()

    if not user:

        return redirect(
            url_for("setup.setup")
        )

    if request.method == "POST":

        new_password = request.form.get(
            "vault_password"
        )

        new_pattern = request.form.get(
            "calendar_pattern"
        )

        user.vault_password = generate_password_hash(
            new_password
        )

        user.calendar_pattern = new_pattern

        db.session.commit()

        return redirect(
            url_for("calendar.home")
        )

    return render_template(
        "auth/reset_access.html"
    )