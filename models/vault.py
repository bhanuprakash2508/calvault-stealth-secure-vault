from datetime import datetime
from extensions import db

class VaultEntry(db.Model):

    __tablename__ = "vault_entries"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    site_name = db.Column(
        db.String(100),
        nullable=False
    )

    site_username = db.Column(
        db.String(120),
        nullable=False
    )

    encrypted_password = db.Column(
        db.Text,
        nullable=False
    )

    category = db.Column(
        db.String(50),
        default="Other"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )