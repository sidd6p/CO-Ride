from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SubmitField
from wtforms.validators import Length, DataRequired

class MyFeedback(FlaskForm):
    title = StringField('Title', validators=[Length(min=5, max=50), DataRequired()])
    content = TextAreaField('Feedback', validators=[Length(min=10, max=500)])
    date = DateField('Feed back date', format='%m/%d/%Y', validators=[DataRequired()])
    submit = SubmitField('Send Feedback')
