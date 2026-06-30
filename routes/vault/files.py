from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_file
)

from models.file import VaultFile
from extensions import db

from services.encryption_service import (
    encrypt_file,
    decrypt_file
)

from services.activity_service import log_activity

from werkzeug.utils import secure_filename
from io import BytesIO

import os
import uuid


files_bp = Blueprint(
    "files",
    __name__
)

# File Vault

@files_bp.route("/file-vault")
def file_vault():

    if not session.get("vault_access"):

        return redirect(
            url_for("calendar.home")
        )

    page = request.args.get(
        "page",
        1,
        type=int
    )

    files = VaultFile.query.filter_by(
        user_id=1
    ).paginate(
        page=page,
        per_page=9,
        error_out=False
    )

    return render_template(
        "vault/file_vault.html",
        files=files.items,
        pagination=files
    )

# Upload File

@files_bp.route(
    "/upload-file",
    methods=["POST"]
)
def upload_file():

    if not session.get("vault_access"):

        return redirect(
            url_for("calendar.home")
        )

    uploaded_file = request.files.get("file")

    if uploaded_file:

        original_filename = secure_filename(
            uploaded_file.filename
        )

        file_data = uploaded_file.read()

        encrypted_data = encrypt_file(
            file_data
        )

        encrypted_filename = (
            str(uuid.uuid4()) + ".enc"
        )

        filepath = os.path.join(
            "uploads",
            encrypted_filename
        )

        with open(filepath, "wb") as f:
            f.write(encrypted_data)

        file_entry = VaultFile(
            user_id=1,
            original_filename=original_filename,
            encrypted_filename=encrypted_filename
        )

        db.session.add(file_entry)
        db.session.commit()

        log_activity(
            f"📁 File Uploaded → {original_filename}"
        )

    return redirect(
        url_for("files.file_vault")
    )

# Download File

@files_bp.route(
    "/download-file/<int:id>"
)
def download_file(id):

    if not session.get("vault_access"):

        return redirect(
            url_for("calendar.home")
        )

    file = VaultFile.query.filter_by(
        id=id
    ).first()

    if not file:

        return redirect(
            url_for("files.file_vault")
        )

    filepath = os.path.join(
        "uploads",
        file.encrypted_filename
    )

    # FIX ADDED
    if not os.path.exists(filepath):

        return redirect(
            url_for("files.file_vault")
        )

    with open(filepath, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = decrypt_file(
        encrypted_data
    )

    return send_file(
        BytesIO(decrypted_data),
        as_attachment=True,
        download_name=file.original_filename
    )

# Delete File

@files_bp.route(
    "/delete-file/<int:id>",
    methods=["POST"]
)
def delete_file(id):

    if not session.get("vault_access"):

        return redirect(
            url_for("calendar.home")
        )

    file = VaultFile.query.filter_by(
        id=id
    ).first()

    if file:

        filepath = os.path.join(
            "uploads",
            file.encrypted_filename
        )

        if os.path.exists(filepath):

            os.remove(filepath)

        db.session.delete(file)
        db.session.commit()

        log_activity(
            f"🗑 File Deleted → {file.original_filename}"
        )

    return redirect(
        url_for("files.file_vault")
    )

# Preview File

@files_bp.route(
    "/preview-file/<int:id>"
)
def preview_file(id):

    if not session.get("vault_access"):

        return redirect(
            url_for("calendar.home")
        )

    file = VaultFile.query.filter_by(
        id=id
    ).first()

    if not file:

        return redirect(
            url_for("files.file_vault")
        )

    filepath = os.path.join(
        "uploads",
        file.encrypted_filename
    )

    # FIX ADDED
    if not os.path.exists(filepath):

        return redirect(
            url_for("files.file_vault")
        )

    with open(filepath, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = decrypt_file(
        encrypted_data
    )

    extension = file.original_filename.split(
        "."
    )[-1].lower()

    mime_type = "application/octet-stream"

    if extension == "pdf":

        mime_type = "application/pdf"

    elif extension in [
        "png",
        "jpg",
        "jpeg"
    ]:

        mime_type = f"image/{extension}"

    elif extension == "txt":

        mime_type = "text/plain"

    return send_file(
        BytesIO(decrypted_data),
        mimetype=mime_type,
        as_attachment=False
    )