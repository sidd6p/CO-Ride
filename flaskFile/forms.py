from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, NumberRange
from flaskFile.models import User
from flask_login import current_user
from datetime import datetime

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class Ride(FlaskForm):
    source = StringField('Source', validators=[DataRequired()])
    destination = StringField('Destination', validators=[DataRequired()])
    date = DateField('Start Date', format='%m/%d/%Y', validators=[DataRequired()])
    preference = SelectField('Preference', choices=['', 'Rating', 'Verified'])
    submit = SubmitField('Find Ride')

    def validate_destination(self, destination):
        if self.source.data == self.destination.data:
            raise ValidationError("Destination and Source cannot be same")
    
    def validate_date(self, date):
        if date.data <= datetime.date(datetime.utcnow()):
            raise ValidationError("Invalid date of Ride")



class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=2, max=20)])
    email = StringField('Email', validators=[Email()])
    picture = FileField("Profile picture", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data:
            user = User.query.filter_by(username=username.data).first()
            if user and username.data != current_user.username:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data:
            emails = User.query.filter_by(email=email.data).first()
            if emails and email.data != current_user.email:
                raise ValidationError('That email is taken. Please choose a different one.')

class MyFeedback(FlaskForm):
    title = StringField('Title', validators=[Length(min=5, max=50), DataRequired()])
    content = TextAreaField('Feedback', validators=[Length(min=10, max=500)])
    date = DateField('Feed back date', format='%m/%d/%Y', validators=[DataRequired()])
    submit = SubmitField('Send Feedback')
