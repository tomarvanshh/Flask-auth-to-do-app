# routes/__init__.py
# This file registers all route blueprints

from flask import Blueprint
from .auth import auth_bp
from .tasks import tasks_bp

# Create a main blueprint that combines all sub-blueprints
# All routes from auth_bp and tasks_bp will be available under this main blueprint
def register_routes(app):
    """
    Register all route blueprints with the Flask app
    
    Args:
        app: Flask application instance
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
