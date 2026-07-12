from src.routes import routes
from flask import jsonify


# health-check route
@routes.route("/health")
def health():
    return jsonify(status='ok')
