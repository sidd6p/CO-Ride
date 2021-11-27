from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime

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

