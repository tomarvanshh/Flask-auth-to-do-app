# This is where we setup the engine of the app
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    app.secret_key = os.getenv('SECRET_KEY')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME', 'vanshdb')  # default to vanshdb if DB_NAME is not provided
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{db_user}:{db_password}@localhost/{db_name}"
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # if user not logged in, redirect to login page

    # Import models so SQLAlchemy knows about them when creating tables
    # Models are now in the models/ directory with __init__.py that exports them
    from .models import User, Task

    # Register all route blueprints
    # Routes are now organized in routes/ directory with separate files for auth and tasks
    from .routes import register_routes
    register_routes(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))