from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
from wtforms import TextAreaField, SelectMultipleField

from flask_wtf import FlaskForm

from app import app, tag_choices
from app.models import *

    
class PhotoForm(FlaskForm):
    photo_title = StringField('Photo title', validators=[DataRequired()])
    photo_description = TextAreaField('Photo about', validators=[DataRequired()])
    tags = RadioField(
        'Select tags', choices=tag_choices, validators=[DataRequired()])
    submit = SubmitField('Submit')