from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from models.vault import VaultEntry
from extensions import db

from services.encryption_service import (
    encrypt_data,
    decrypt_data
)

from services.activity_service import log_activity

passwords_bp = Blueprint(
    "passwords",
    __name__
)

# PASSWORD VAULT

@passwords_bp.route("/password-vault")
def password_vault():

    if not session.get("vault_access"):

        return redirect(
            url_for("calendar.home")
        )

    page = request.args.get(
        "page",
        1,
        type=int
    )

    vault_entries = VaultEntry.query.paginate(
        page=page,
        per_page=8,
        error_out=False
    )

    entries = []

    for item in vault_entries.items:

        entries.append(
            {
                "id": item.id,
                "name": item.site_name,
                "username": item.site_username,
                "password": decrypt_data(
                    item.encrypted_password
                ),
                "category": item.category
            }
        )

    return render_template(
        "vault/password_vault.html",
        entries=entries,
        pagination=vault_entries
    )

# ADD PASSWORD

@passwords_bp.route(
    "/add-entry",
    methods=["POST"]
)
def add_entry():

    if not session.get("vault_access"):

        return redirect(
            url_for("calendar.home")
        )

    site_name = request.form.get("name")
    site_username = request.form.get("username")
    password = request.form.get("password")
    category = request.form.get("category")

    encrypted_password = encrypt_data(
        password
    )

    entry = VaultEntry(
        user_id=1,
        site_name=site_name,
        site_username=site_username,
        encrypted_password=encrypted_password,
        category=category
    )

    db.session.add(entry)
    db.session.commit()

    log_activity(
        f"🔑 Password Added → {site_name}"
    )

    return redirect(
        url_for("passwords.password_vault")
    )

# EDIT PASSWORD

@passwords_bp.route(
    "/edit-entry/<int:id>",
    methods=["POST"]
)
def edit_entry(id):

    if not session.get("vault_access"):

        return redirect(
            url_for("calendar.home")
        )

    entry = VaultEntry.query.filter_by(
        id=id
    ).first()

    if not entry:

        return redirect(
            url_for("passwords.password_vault")
        )

    entry.site_name = request.form.get(
        "name"
    )

    entry.site_username = request.form.get(
        "username"
    )

    entry.encrypted_password = encrypt_data(
        request.form.get("password")
    )

    entry.category = request.form.get(
        "category"
    )

    db.session.commit()

    log_activity(
        f"✏ Password Updated → {entry.site_name}"
    )

    return redirect(
        url_for("passwords.password_vault")
    )

# DELETE PASSWORD

@passwords_bp.route(
    "/delete-entry/<int:id>",
    methods=["POST"]
)
def delete_entry(id):

    if not session.get("vault_access"):

        return redirect(
            url_for("calendar.home")
        )

    entry = VaultEntry.query.filter_by(
        id=id
    ).first()

    if entry:

        log_activity(
            f"🗑 Password Deleted → {entry.site_name}"
        )

        db.session.delete(entry)
        db.session.commit()

    return redirect(
        url_for("passwords.password_vault")
    )