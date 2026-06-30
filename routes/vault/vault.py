from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_file
)

from werkzeug.security import (
    check_password_hash
)

from models.user import User
from models.vault import VaultEntry
from models.file import VaultFile
from models.activity import ActivityLog

from services.encryption_service import (
    encrypt_data,
    decrypt_data
)

from services.activity_service import log_activity

from extensions import db
from io import BytesIO

import json
import os

vault_bp = Blueprint(
    "vault",
    __name__
)

# Vault Password Page

@vault_bp.route(
    "/vault-auth",
    methods=["GET", "POST"]
)
def vault_auth():

    if not session.get("pattern_verified"):
        return redirect(
            url_for("calendar.home")
        )

    if request.method == "POST":

        password = request.form.get(
            "vault_password"
        )

        user = User.query.first()

        if check_password_hash(
            user.vault_password,
            password
        ):

            session["vault_access"] = True

            log_activity(
                "🔓 Vault Unlocked"
            )

            session.pop(
                "pattern_verified",
                None
            )

            return redirect(
                url_for("vault.vault")
            )

        return redirect(
            url_for("calendar.home")
        )

    return render_template(
        "auth/vault_auth.html"
    )

# Main Vault

@vault_bp.route("/vault")
def vault():

    if not session.get("vault_access"):
        return redirect(
            url_for("calendar.home")
        )

    passwords_count = VaultEntry.query.count()
    files_count = VaultFile.query.count()

    return render_template(
        "vault/vault.html",
        passwords_count=passwords_count,
        files_count=files_count
    )

# Export Backup

@vault_bp.route("/export-backup")
def export_backup():

    if not session.get("vault_access"):
        return redirect(
            url_for("calendar.home")
        )

    password_entries = VaultEntry.query.filter_by(
        user_id=1
    ).all()

    file_entries = VaultFile.query.filter_by(
        user_id=1
    ).all()

    backup_data = {
        "passwords": [],
        "files": []
    }

    log_activity(
        "💾 Backup Exported"
    )

    # Password backup

    for item in password_entries:

        backup_data["passwords"].append(
            {
                "site_name": item.site_name,
                "site_username": item.site_username,
                "encrypted_password": item.encrypted_password,
                "category": item.category
            }
        )

    # File backup (INCLUDING REAL FILE DATA)

    for file in file_entries:

        filepath = os.path.join(
            "uploads",
            file.encrypted_filename
        )

        if os.path.exists(filepath):

            with open(filepath, "rb") as f:
                encrypted_file_data = f.read()

            backup_data["files"].append(
                {
                    "original_filename": file.original_filename,
                    "encrypted_filename": file.encrypted_filename,
                    "file_data": encrypted_file_data.hex()
                }
            )

    json_data = json.dumps(
        backup_data
    )

    encrypted_backup = encrypt_data(
        json_data
    )

    return send_file(
        BytesIO(
            encrypted_backup.encode()
        ),
        as_attachment=True,
        download_name="calvault_backup.enc",
        mimetype="application/octet-stream"
    )

# Restore Backup

@vault_bp.route(
    "/restore-backup",
    methods=["POST"]
)
def restore_backup():

    if not session.get("vault_access"):
        return redirect(
            url_for("calendar.home")
        )

    backup_file = request.files.get(
        "backup_file"
    )

    if not backup_file:
        return redirect(
            url_for("vault.vault")
        )

    encrypted_data = backup_file.read().decode()

    decrypted_json = decrypt_data(
        encrypted_data
    )

    backup_data = json.loads(
        decrypted_json
    )

    log_activity(
        "♻ Backup Restored"
    )

    # Restore passwords

    for item in backup_data["passwords"]:

        entry = VaultEntry(
            user_id=1,
            site_name=item["site_name"],
            site_username=item["site_username"],
            encrypted_password=item["encrypted_password"],
            category=item["category"]
        )

        db.session.add(entry)

    # Restore files + recreate physical encrypted files

    for file in backup_data["files"]:

        file_entry = VaultFile(
            user_id=1,
            original_filename=file["original_filename"],
            encrypted_filename=file["encrypted_filename"]
        )

        db.session.add(file_entry)

        file_bytes = bytes.fromhex(
            file["file_data"]
        )

        filepath = os.path.join(
            "uploads",
            file["encrypted_filename"]
        )

        with open(filepath, "wb") as f:
            f.write(file_bytes)

    db.session.commit()

    return redirect(
        url_for("vault.vault")
    )

# Delete Account

@vault_bp.route(
    "/delete-account",
    methods=["GET", "POST"]
)
def delete_account():

    if not session.get("vault_access"):
        return redirect(
            url_for("calendar.home")
        )

    user = User.query.first()

    if request.method == "POST":

        password = request.form.get(
            "vault_password"
        )

        if not check_password_hash(
            user.vault_password,
            password
        ):

            error = "Incorrect Vault Password"

            return render_template(
                "settings/delete_account.html",
                error=error
            )

        entries = VaultEntry.query.all()

        for entry in entries:
            db.session.delete(entry)

        files = VaultFile.query.all()

        for file in files:

            filepath = os.path.join(
                "uploads",
                file.encrypted_filename
            )

            if os.path.exists(filepath):
                os.remove(filepath)

            db.session.delete(file)

        db.session.delete(user)
        db.session.commit()

        session.clear()

        return redirect("/")

    return render_template(
        "settings/delete_account.html"
    )

@vault_bp.route("/lock-vault")
def lock_vault():

    session.pop(
        "vault_access",
        None
    )

    session.pop(
        "pattern_verified",
        None
    )

    return redirect(
        url_for("calendar.home")
    )

@vault_bp.route("/activity-log")
def activity_log():

    if not session.get("vault_access"):
        return redirect(
            url_for("calendar.home")
        )

    logs = ActivityLog.query.order_by(
        ActivityLog.timestamp.desc()
    ).all()

    return render_template(
        "vault/activity_log.html",
        logs=logs
    )

@vault_bp.route(
    "/clear-activity",
    methods=["POST"]
)
def clear_activity():

    if not session.get("vault_access"):
        return redirect(
            url_for("calendar.home")
        )

    ActivityLog.query.delete()
    db.session.commit()

    return redirect(
        url_for("vault.activity_log")
    )