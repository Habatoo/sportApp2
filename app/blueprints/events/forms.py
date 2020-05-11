from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
from wtforms import TextAreaField
from wtforms.fields.html5 import DateTimeField

from flask_wtf import FlaskForm

from app.models import *
from app import app


class EventForm(FlaskForm):
    event_title = StringField('Title', validators=[DataRequired()])
    event_body = TextAreaField('Event', validators=[DataRequired()])
    event_time = DateTimeField(
        'Which date is your favorite?', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    event_place = TextAreaField('Place, adress', validators=[DataRequired()])
    event_geo = TextAreaField('GEO, long, lat', validators=[DataRequired()])
    tags = RadioField(
        'Select tags', choices=[(tag.name, tag.slug) for tag in Tag.query.all()], validators=[DataRequired()])
    submit = SubmitField('Submit')

    # id = db.Column(db.Integer, primary_key=True)
    # event_title = db.Column(db.String(140))
    # event_body = db.Column(db.Text)
    # slug = db.Column(db.String(140), unique=True)
    # created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    # event_time = db.Column(db.DateTime)
    # event_place = db.Column(db.Text)
    # event_geo = db.Column(db.Text)

    # event_starter = db.Column(db.Integer, db.ForeignKey('user.id'))
    # event_crew = db.Column(db.Integer, db.ForeignKey('user.id'))