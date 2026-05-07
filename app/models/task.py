# models/task.py
# Task database model for todo list items

from app import db
from datetime import datetime

class Task(db.Model):
    """
    Task model for todo items.
    Each task belongs to a user and has a status that can be: Pending, Working, or Completed.
    
    Attributes:
        id: Unique task identifier (Primary Key)
        title: Task title/description
        status: Task status (Pending, Working, Completed)
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
        user_id: Foreign key linking to the User table
    
    Relationship:
        - user_id: Foreign key to the User table (many tasks belong to one user)
    """
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  # The task title/description
    status = db.Column(db.String(20), default='Pending')  # Status: Pending, Working, or Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # When the task was created
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # When last updated
    
    # Foreign key linking to the User table (each task belongs to a user)
    # This ensures only the user who created a task can modify it
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        """String representation of the task for debugging"""
        return f'<Task {self.id}: {self.title} - {self.status}>'
