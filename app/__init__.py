# This is where we setup the engine of the app
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import pymysql
pymysql.install_as_MySQLdb()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    app.secret_key = os.getenv('SECRET_KEY')

    cloud_db = os.getenv('DATABASE_URL')
    if not cloud_db:
        raise RuntimeError('DATABASE_URL is required for cloud database deployment.')

    app.config['SQLALCHEMY_DATABASE_URI'] = cloud_db
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    with app.app_context():
        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))