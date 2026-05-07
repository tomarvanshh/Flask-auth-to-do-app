# models/user.py
# User database model for authentication

from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """
    User model for authentication and task management.
    Each user can have multiple tasks (one-to-many relationship).
    
    Attributes:
        id: Unique user identifier (Primary Key)
        name: User's full name
        email: Unique email address for login
        password: Bcrypt-hashed password (never stored in plaintext)
        tasks: Relationship to Task model (one user has many tasks)
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    # Relationship to tasks: one user has many tasks
    # back_populates creates a bidirectional relationship so we can access user from task too
    # cascade='all, delete-orphan' means if user is deleted, all their tasks are deleted too
    tasks = db.relationship('Task', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        """String representation for debugging"""
        return f'<User {self.id}: {self.email}>'
