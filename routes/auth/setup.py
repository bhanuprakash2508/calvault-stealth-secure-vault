from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from werkzeug.security import (
    generate_password_hash
)

from models.user import User
from extensions import db

from services.recovery_service import generate_recovery_key

setup_bp = Blueprint(
    "setup",
    __name__
)

# Setup Page

@setup_bp.route(
    "/setup",
    methods=["GET", "POST"]
)
def setup():

    existing_user = User.query.first()

    if existing_user:

        return redirect(
            url_for("calendar.home")
        )

    if request.method == "POST":

        vault_password = request.form.get(
            "vault_password"
        )

        calendar_pattern = request.form.get(
            "calendar_pattern"
        )

        hashed_password = generate_password_hash(
            vault_password
        )

        recovery_key = generate_recovery_key()

        user = User(

            vault_password=hashed_password,
            calendar_pattern=calendar_pattern,
            recovery_key=recovery_key,
            setup_completed=True
        )

        db.session.add(user)
        db.session.commit()

        return render_template(
            "auth/recovery_key.html",
            recovery_key=recovery_key
        )

    return render_template(
        "auth/setup.html"
    )