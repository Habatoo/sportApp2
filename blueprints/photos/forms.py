from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
from wtforms import TextAreaField, SelectMultipleField

from flask_wtf import FlaskForm

from app import app
from models import *


class PhotoForm(FlaskForm):
    pass