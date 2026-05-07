# routes/tasks.py
# Task management routes: create, read, update, delete tasks

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Task
from app import db

# Create a blueprint for task routes
tasks_bp = Blueprint('tasks', __name__, url_prefix='')

@tasks_bp.route('/dashboard')
@login_required  # This decorator ensures that only logged-in users can access the dashboard route
def dashboard():
    """
    Dashboard route - shows user profile and their tasks
    @login_required: Redirects non-authenticated users to login page
    
    Returns:
        Renders the dashboard template with current user and their tasks
    """
    # Get all tasks for the current logged-in user (using the relationship we created)
    user_tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', user=current_user, tasks=user_tasks)


@tasks_bp.route('/tasks/add', methods=['POST'])
@login_required
def add_task():
    """
    Add new task route
    
    POST: Creates a new task for the logged-in user
    Gets title from form, creates Task object with user_id set to current_user.id
    """
    title = request.form.get('title', '').strip()  # Get title from form and remove extra spaces
    
    # Validate: title should not be empty
    if title:
        # Create a new task and link it to the current user using user_id
        new_task = Task(title=title, status='Pending', user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully!", "success")
    else:
        flash("Task title cannot be empty!", "danger")
    
    return redirect(url_for('tasks.dashboard'))


@tasks_bp.route('/tasks/update/<int:task_id>', methods=['POST'])
@login_required
def update_task_status(task_id):
    """
    Update task status route
    
    Cycles through statuses: Pending -> Working -> Completed -> Pending
    SECURITY: Checks that task belongs to current_user (prevents users from modifying others' tasks)
    """
    task = Task.query.get(task_id)
    
    # Security check: ensure the task belongs to the current user
    if task and task.user_id == current_user.id:
        # Cycle through the three statuses
        if task.status == 'Pending':
            task.status = 'Working'
        elif task.status == 'Working':
            task.status = 'Completed'
        else:
            task.status = 'Pending'
        
        db.session.commit()
        flash("Task status updated!", "success")
    elif task and task.user_id != current_user.id:
        flash("You don't have permission to modify this task!", "danger")
    else:
        flash("Task not found!", "danger")
    
    return redirect(url_for('tasks.dashboard'))


@tasks_bp.route('/tasks/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    """
    Delete task route
    
    Deletes a specific task
    SECURITY: Checks that task belongs to current_user before deletion
    """
    task = Task.query.get(task_id)
    
    # Security check: ensure the task belongs to the current user
    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted successfully!", "success")
    elif task and task.user_id != current_user.id:
        flash("You don't have permission to delete this task!", "danger")
    else:
        flash("Task not found!", "danger")
    
    return redirect(url_for('tasks.dashboard'))


@tasks_bp.route('/tasks/clear', methods=['POST'])
@login_required
def clear_all_tasks():
    """
    Clear all tasks route
    
    Deletes ALL tasks belonging to the current user
    WARNING: This action cannot be undone
    """
    # Query only tasks that belong to current_user (secure - can't delete others' tasks)
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    for task in tasks:
        db.session.delete(task)
    
    db.session.commit()
    flash("All tasks cleared successfully!", "success")
    return redirect(url_for('tasks.dashboard'))
