from flask import Flask
import os

from config import Config
from extensions import db

# AUTH ROUTES

from routes.auth.setup import setup_bp

# CALENDAR ROUTES

from routes.calendar.calendar import calendar_bp
from routes.calendar.hidden import hidden_bp

# VAULT ROUTES

from routes.vault.vault import vault_bp
from routes.vault.passwords import passwords_bp
from routes.vault.files import files_bp
from routes.vault.recovery import recovery_bp

# SETTINGS ROUTES

from routes.settings.settings import settings_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    # Register Blueprints

    app.register_blueprint(setup_bp)

    app.register_blueprint(calendar_bp)

    app.register_blueprint(hidden_bp)

    app.register_blueprint(vault_bp)

    app.register_blueprint(passwords_bp)

    app.register_blueprint(files_bp)

    app.register_blueprint(recovery_bp)

    app.register_blueprint(settings_bp)

    # Create Database

    with app.app_context():

        os.makedirs(
            "instance",
            exist_ok=True
        )

        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":

    app.run(
        debug=True
    )