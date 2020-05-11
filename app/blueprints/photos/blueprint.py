from flask import Blueprint
from flask import render_template
from flask import flash, redirect
from flask import redirect
from flask import url_for
from flask import request

from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import login_required

from .forms import PhotoForm

from app import app
from app import db
from app.models import *

photos = Blueprint('photos', __name__, template_folder='templates')

@photos.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('photos/index.html')