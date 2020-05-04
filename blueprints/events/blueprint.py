from flask import Blueprint
from flask import render_template

events = Blueprint('events', __name__, template_folder='templates')

@events.route('/')
def index():
    return render_template('events/index.html')