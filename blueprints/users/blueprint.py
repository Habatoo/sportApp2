from flask import Blueprint
from flask import render_template

users = Blueprint('users', __name__, template_folder='templates')

@users.route('/')
def index():
    return render_template('users/index.html')