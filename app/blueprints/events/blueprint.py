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

from .forms import EventForm

from app import app
from app import db
from app import log
from app.models import *

try:
    from geopy.geocoders import Nominatim
except:
    redirect('events.index')


events = Blueprint('events', __name__, template_folder='templates')

@events.route('/event_new', methods=['GET', 'POST'])
@login_required
def event_new():
    form = EventForm()
    if request.args == '':
        return redirect('')
    if request.method == 'GET':
        place = request.args
        geolocator = Nominatim(user_agent='habatoo@yandex.ru') 
        location = geolocator.geocode(place.get('search', default = None))
        if location:
            newLocation = str(location.latitude) + str(", ") + str(location.longitude)  
            location_geo = geolocator.reverse([location.latitude, location.longitude]) # 37.62, 55.75
            address = location_geo.address
            event = Event(
            event_title=None, 
            event_body=None, 
            event_time=None,
            event_place = address,
            event_geo = newLocation,
            event_level = None,
            event_author=current_user)
            form = EventForm(
                formdata=request.form, obj=event)
            return render_template('events/new_event.html', form=form)
        else:
            print('no search')
            return redirect('')          

    if form.validate_on_submit():
        event = Event(
            event_title=form.event_title.data, 
            event_body=form.event_body.data, 
            event_time= form.event_time.data,
            event_place = form.event_place.data,
            event_geo = form.event_geo.data,
            event_level = form.event_level.data,
            event_author=current_user)
        event.tags.append(Tag.query.filter_by(name=form.tags.data).first())
        #try:
        db.session.commit()
        flash('Your cane make event!')
        return redirect(url_for('events.index'))
        #except:
        #    redirect('index') # create!!!
    return render_template('events/new_event.html', form=form)

@events.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(slug):
    event = Event.query.filter(Event.slug==slug).first()
    form = EventForm(formdata=request.form, obj=event)

    if form.validate_on_submit():
        event.event_title=form.event_title.data
        event.event_body=form.event_body.data 
        event.event_time= form.event_time.data
        event.event_place = form.event_place.data
        event.event_geo = form.event_geo.data
        event.event_level = form.event_level.data
        try:
            event.tags.append(Tag.query.filter_by(name=form.tags.data).first())
            db.session.commit()
            flash('Your event edited')
            log.info("User '%s' edit event '%s'." % (current_user.username, event.event_title))
            return redirect(url_for('events.event_detail', slug=event.slug))
        except:
           redirect('events.index') 
    form = EventForm(obj=event)
    return render_template('events/edit_event.html', form=form)

@events.route('/', methods=['GET', 'POST'])
@login_required
def index():
    q = request.args.get('q')
    page = request.args.get('page')
    page = request.args.get('page', 1, type=int)
    if q:
        events = Event.query.filter(Event.event_title.contains(q) | Event.event_body.contains(q).all())
    else:
        events = Event.query.order_by(Event.created.desc())
        
    pages = events.paginate(page=page, per_page=app.config['POSTS_PER_PAGE'])

    return render_template('events/index.html', pages=pages)


@events.route('/<slug>')
@login_required
def event_detail(slug):
    event = Event.query.filter(Event.slug==slug).first()
    tags = event.tags
    return render_template('events/event_detail.html', event=event, tags=tags)

@events.route('/tag/<slug>')
@login_required
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug==slug).first()
    events = tag.events_tags.all()
    return render_template('events/tag_detail.html', tag=tag, events=events)