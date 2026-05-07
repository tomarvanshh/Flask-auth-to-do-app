from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from flask_login import current_user

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()]) # first argument "Name" is the label for the form field, and validators is a list of validation rules that will be applied to this field when the form is submitted. In this case, DataRequired() ensures that the user cannot submit the form without filling out this field.
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):    # Flask-WTF automatically recognizes methods named validate_<fieldname>() and runs them during form validation, validate_email() is automatically called when validating the email field.
        from .models import User        # This checks if there's already a user with the same email in the database. If there is, it raises a ValidationError, which will be displayed to the user.
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists.")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password (leave blank to keep current password)')
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password',message='Passwords must match')])
    submit = SubmitField('Update Profile')

    # check if the new email is already taken by another user (excluding the current user)
    def validate_email(self, email):
        if email.data != current_user.email: #why current_user is red error:  # Only check if the email is different from the current user's email
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email already exists. Please choose a different one.")