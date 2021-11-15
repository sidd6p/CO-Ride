from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flaskFile.models import User
from flask_login import current_user

#inherited from FlaskForm class
class RegistrationForm(FlaskForm):
    #The SubmitField class represents an <input> element with a type="submit" attribute.
    # The first argument to the Field constructors is the label that will be used when rendering the form to HTML.
    #These are the attributes of RegestrationForm class
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


class UpdateAccountForm(FlaskForm):
    #The SubmitField class represents an <input> element with a type="submit" attribute.
    # The first argument to the Field constructors is the label that will be used when rendering the form to HTML.
    #These are the attributes of RegestrationForm class
    username = StringField('Username', validators=[Length(min=2, max=20)])
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data:
            if username.data == current_user.username:
                raise ValidationError("New Username cannot same as current Username")
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data:
            if email.data == current_user.email:
                raise ValidationError("New Email cannot same as current Email")
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken. Please choose a different one.')
