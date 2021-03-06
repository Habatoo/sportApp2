from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
from wtforms import TextAreaField
from wtforms.fields.html5 import DateTimeField

from flask_wtf import FlaskForm

from app import app, tag_choices
from app.models import *


class EventForm(FlaskForm):
    event_title = StringField('Title', validators=[DataRequired()])
    event_body = TextAreaField('Event', validators=[DataRequired()])
    event_time = DateTimeField(
        'Select date of event', format='%Y-%m-%d %H:%M:%S')#, validators=[DataRequired()])
    event_place = TextAreaField('Place, address', validators=[DataRequired()])
    event_geo = TextAreaField('GEO, long, lat', validators=[DataRequired()])
    event_level = StringField('Event level', validators=[DataRequired()])
    tags = RadioField(
        'Select tags', choices=tag_choices)
    # event_crew = db.Column(db.Integer, db.ForeignKey('user.id'))
    submit = SubmitField('Submit')
