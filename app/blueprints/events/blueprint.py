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
from app.models import *

events = Blueprint('events', __name__, template_folder='templates')

@events.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(slug):
    event = Event.query.filter(Event.slug==slug).first()
    form = EventForm(formdata=request.form, obj=event)

    if form.validate_on_submit():
        event_title=form.event_title.data, 
        event_body=form.event_body.data, 
        event_time= form.event_time.data,
        event_place = form.event_place.data,
        event_geo = form.event_geo.data,
        try:
            event.tags.append(Tag.query.filter_by(name=form.tags.data).first())
            db.session.commit()
            flash('Your event edited')
            return redirect(url_for('events.event_detail', slug=event.slug))
        except:
           redirect('events.index') 
    form = EventForm(obj=event)
    return render_template('events/edit_event.html', form=form)

@events.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            event_title=form.event_title.data, 
            event_body=form.event_body.data, 
            event_time= form.event_time.data,
            event_place = form.event_place.data,
            event_geo = form.event_geo.data,
            event_author=current_user)
        #try:
        event.tags.append(Tag.query.filter_by(name=form.tags.data).first())
        db.session.commit()
        flash('Your cane make event!')
        return redirect(url_for('events.index'))
        #except:
        #    redirect('index') # create!!!

    q = request.args.get('q')
    page = request.args.get('page')
    page = request.args.get('page', 1, type=int)
    # if page and page.isdigit():
    #     page = int(page) 
    # else:
    #     page = 1 
    if q:
        events = Event.query.filter(Event.event_title.contains(q) | Event.event_body.contains(q).all())
    else:
        events = Event.query.order_by(Event.created.desc())
        
    pages = events.paginate(page=page, per_page=app.config['POSTS_PER_PAGE'])

    return render_template('events/index.html', form=form, pages=pages)


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