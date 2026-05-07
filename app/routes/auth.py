# routes/auth.py
# Authentication routes: register, login, logout, profile management

from flask import Blueprint, render_template, redirect, url_for, flash, request
import bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegisterForm, LoginForm, UpdateAccountForm
from app.models import User
from app import db

# Create a blueprint for authentication routes
# A blueprint is a way to group related routes together
auth_bp = Blueprint('auth', __name__, url_prefix='')

@auth_bp.route('/')
def home():
    """Home page - accessible to everyone"""
    return render_template('index.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registration route - allows new users to create an account
    
    GET: Displays the registration form
    POST: Hashes password with bcrypt and creates new user in database
    """
    form = RegisterForm()
    if form.validate_on_submit():
        # Bcrypt: Convert password to hash so we never store plain passwords
        hashed = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(name=form.name.data, email=form.email.data, password=hashed)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created!", "success")
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login route - authenticates user and creates session
    
    GET: Displays the login form
    POST: Checks email and password, logs user in if credentials match
    """
    form = LoginForm()
    if form.validate_on_submit():
        # Query the database using the model
        user = User.query.filter_by(email=form.email.data).first()
        # Check if user exists AND password matches (bcrypt.checkpw validates hashed password)
        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)  # This will log the user in and create a session for them.
            flash("Login successful!", "success")
            return redirect(url_for('tasks.dashboard'))  # Redirect to the dashboard after successful login
        else:
            flash("Invalid email or password. Please try again.", "danger")
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout route - clears user session"""
    logout_user()  # This will log the user out and clear their session.
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Profile route - allows user to update their profile (name, email, password)
    
    GET: Pre-fills form with current user data
    POST: Updates user information in database
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # update name and email
        current_user.name = form.name.data
        current_user.email = form.email.data

        if form.password.data:  # if the user entered a new password
            hashed_pw = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            current_user.password = hashed_pw

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('tasks.dashboard'))
    
    # Pre-fill the form with current user data when the page loads (GET request)
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email

    return render_template('profile.html', form=form)
