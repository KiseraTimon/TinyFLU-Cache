from src.routes import routes
from flask import jsonify


# homepage route
@routes.route("/")
def homepage():
    return "Home Page is OK"

# health-check route
@routes.route("/health")
def health():
    return jsonify(status='ok')
