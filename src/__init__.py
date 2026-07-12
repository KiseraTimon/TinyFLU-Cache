from __future__ import annotations
from flask import Flask
from dotenv import load_dotenv
import os

from config import Default, Development, Production
from utilities import log_critical_error, log_system_info


# Configurations Map
CONFIG_MAP = {
    "production": Production,
    "development": Development,
}


# flask factory
def create_app() -> Flask:
    # loading environment vars
    load_dotenv()

    # flask access mode
    mode = str(os.getenv("FLASK_MODE", "")
    ).strip().lower()

    # flask object
    app = Flask(__name__)

    # applying configurations
    app.config.from_object(CONFIG_MAP.get(mode, Default))

    # routes
    from src.routes import routes
    app.register_blueprint(routes, url_prefix="/")

    # global web exception handler
    @app.errorhandler(Exception)
    def handle_unhandled_exception(e):
        # logging full stack trace
        log_critical_error(e, log="unhandled_web_crashes", path="web")

        # error re-raise in dev-mode for interactive Werkzeug debugger
        if app.debug:
            raise e

        # friendly error page in prod-mode
        return "An internal server error occurred.", 500

    return app