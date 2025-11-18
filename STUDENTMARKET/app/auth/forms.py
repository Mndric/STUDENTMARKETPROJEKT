from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    """User registration form"""
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    dob = DateField('Date of Birth', validators=[Optional()], format='%Y-%m-%d')
    description = TextAreaField('About Me', validators=[
        Optional(),
        Length(max=500, message='Description must be less than 500 characters')
    ])
    
    def validate_email(self, field):
        """Check if email already exists"""
        if User.get_by_email(field.data):
            raise ValidationError('Email already registered')


class LoginForm(FlaskForm):
    """User login form"""
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')


class ProfileForm(FlaskForm):
    """User profile edit form"""
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    dob = DateField('Date of Birth', validators=[Optional()], format='%Y-%m-%d')
    description = TextAreaField('About Me', validators=[
        Optional(),
        Length(max=500, message='Description must be less than 500 characters')
    ])
