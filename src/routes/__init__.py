from flask import Blueprint

routes = Blueprint("routes", __name__)

from src.routes import (
    views
)