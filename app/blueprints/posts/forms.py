from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
from wtforms import TextAreaField, SelectMultipleField

from flask_wtf import FlaskForm

from app import app
from app.models import *

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Say something', validators=[DataRequired()])
    tags = RadioField(
        'Select tags', choices=[(tag.name, tag.slug) for tag in Tag.query.all()], validators=[DataRequired()])
    submit = SubmitField('Submit')
