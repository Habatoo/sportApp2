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
from models import *

events = Blueprint('events', __name__, template_folder='templates')

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
        try:
            db.session.add(event)
            db.session.commit()
            flash('Your cane make event!')
            return redirect(url_for('events.index'))
        except:
            redirect('index') # create!!!

    q = request.args.get('q')
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page) 
    else:
        page = 1 
    if q:
        events = Event.query.filter(Event.event_title.contains(q) | Event.event_body.contains(q).all())
    else:
        events = Event.query.order_by(Event.created.desc())
        
    pages = events.paginate(page=page, per_page=app.config['POSTS_PER_PAGE'])

    return render_template('events/index.html', form=form, pages=pages)


# @posts.route('/<slug>/edit', methods=['GET', 'POST'])
# @login_required
# def edit_post(slug):
#     post = Post.query.filter(Post.slug==slug).first()
#     form = PostForm(formdata=request.form, obj=post)

#     if form.validate_on_submit():pages=pages
#         form.populate_obj(post)
#         try:
#             db.session.commit()
#             flash('Your post edited')
#             return redirect(url_for('posts.post_detail', slug=post.slug))
#         except:
#            redirect('posts.index') 
#     form = PostForm(obj=post)
#     return render_template('posts/edit_post.html', form=form)

# @posts.route('/', methods=['GET', 'POST'])
# @login_required
# def index():
#     form = PostForm()
#     if form.validate_on_submit():
#         post = Post(title=form.title.data, body=form.body.data, author=current_user)
#         try:
#             db.session.add(post)
#             db.session.commit()
#             flash('Your post is now live!')
#             return redirect(url_for('posts.index'))
#         except:
#             redirect('posts.create') 

#     q = request.args.get('q')
#     page = request.args.get('page')
#     if page and page.isdigit():
#         page = int(page) 
#     else:
#         page = 1 
#     if q:
#         posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q).all())
#     else:
#         posts = Post.query.order_by(Post.created.desc())
        
#     pages = posts.paginate(page=page, per_page=app.config['POSTS_PER_PAGE'])
#     # max pages = posts.count() or 404
#     return render_template('posts/index.html', form=form, pages=pages)

# @posts.route('/<slug>')
# @login_required
# def post_detail(slug):
#     post = Post.query.filter(Post.slug==slug).first()
#     tags = post.tags
#     return render_template('posts/post_detail.html', post=post, tags=tags)

# @posts.route('/tag/<slug>')
# @login_required
# def tag_detail(slug):
#     tag = Tag.query.filter(Tag.slug==slug).first()
#     posts = tag.posts.all()
#     return render_template('posts/tag_detail.html', tag=tag, posts=posts)