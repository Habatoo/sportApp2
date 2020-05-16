from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
from wtforms import TextAreaField
from wtforms.fields.html5 import DateTimeField

from flask_wtf import FlaskForm

from app import app
from app.models import *



class EventForm(FlaskForm):
    event_title = StringField('Title', validators=[DataRequired()])
    event_body = TextAreaField('Event', validators=[DataRequired()])
    event_time = DateTimeField(
        'Select date of event', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    event_place = TextAreaField('Place, adress', validators=[DataRequired()])
    event_geo = TextAreaField('GEO, long, lat', validators=[DataRequired()])
    tags = RadioField(
        'Select tags', choices=[(tag.name, tag.slug) for tag in Tag.query.all()], validators=[DataRequired()])
    # event_crew = db.Column(db.Integer, db.ForeignKey('user.id'))
    submit = SubmitField('Submit')
