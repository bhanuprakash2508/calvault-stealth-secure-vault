from datetime import datetime
from extensions import db


class VaultFile(db.Model):

    __tablename__ = "vault_files"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    original_filename = db.Column(
        db.String(255),
        nullable=False
    )

    encrypted_filename = db.Column(
        db.String(255),
        nullable=False
    )

    upload_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )