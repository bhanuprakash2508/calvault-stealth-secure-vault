from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

import os

from models.user import User
from models.vault import VaultEntry
from models.file import VaultFile

from extensions import db
from services.activity_service import log_activity

settings_bp = Blueprint(
    "settings",
    __name__
)


@settings_bp.route("/settings")
def settings():

    if not session.get(
        "vault_access"
    ):

        return redirect(
            url_for("calendar.home")
        )

    return render_template(
        "settings/settings.html"
    )


@settings_bp.route(
    "/change-password",
    methods=["GET", "POST"]
)
def change_password():

    if not session.get(
        "vault_access"
    ):

        return redirect(
            url_for("calendar.home")
        )

    user = User.query.first()

    error = None

    if request.method == "POST":

        old_password = request.form.get(
            "old_password"
        )

        new_password = request.form.get(
            "new_password"
        )

        if check_password_hash(
            user.vault_password,
            old_password
        ):

            user.vault_password = generate_password_hash(
                new_password
            )

            db.session.commit()

            log_activity(
                "🔐 Vault Password Changed"
            )

            return redirect(
                url_for("settings.settings")
            )

        else:

            error = "Incorrect Current Password"

    return render_template(
        "settings/change_password.html",
        error=error
    )


@settings_bp.route(
    "/change-pattern",
    methods=["GET", "POST"]
)
def change_pattern():

    if not session.get(
        "vault_access"
    ):

        return redirect(
            url_for("calendar.home")
        )

    user = User.query.first()

    if request.method == "POST":

        new_pattern = request.form.get(
            "calendar_pattern"
        )

        user.calendar_pattern = new_pattern

        db.session.commit()

        log_activity(
            "⚙ Secret Pattern Changed"
        )

        return redirect(
            url_for("settings.settings")
        )

    return render_template(
        "settings/change_pattern.html"
    )

# Reset

@settings_bp.route(
"/reset-vault",
methods=["GET", "POST"]
)
def reset_vault():

    if not session.get(
        "vault_access"
    ):

        return redirect(
            url_for("calendar.home")
        )

    user = User.query.first()

    error = None

    if request.method == "POST":

        entered_password = request.form.get(
            "vault_password"
        )

        if not check_password_hash(

            user.vault_password,
            entered_password
        ):

            error = "Authentication Failed. Incorrect Vault Password."

            return render_template(
                "auth/reset_vault.html",
                error=error
            )

        files = VaultFile.query.all()

        for file in files:

            filepath = os.path.join(

                "uploads",
                file.encrypted_filename
            )

            if os.path.exists(
                filepath
            ):
                os.remove(
                    filepath
                )


        VaultEntry.query.delete()
        VaultFile.query.delete()

        db.session.commit()

        log_activity(
            "⚠ Vault Reset Performed"
        )

        return redirect(
            url_for("vault.vault")
        )

    return render_template(
        "auth/reset_vault.html",
        error=error
    )
