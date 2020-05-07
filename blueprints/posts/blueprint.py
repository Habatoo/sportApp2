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

from .forms import PostForm

from app import app
from app import db
from models import *

posts = Blueprint('posts', __name__, template_folder='templates')

@posts.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(slug):
    post = Post.query.filter(Post.slug==slug).first()
    form = PostForm(formdata=request.form, obj=post)

    if form.validate_on_submit():
        form.populate_obj(post)
        try:
            db.session.commit()
            flash('Your post edited')
            return redirect(url_for('posts.post_detail', slug=post.slug))
        except:
           redirect('posts.index') 
    form = PostForm(obj=post)
    return render_template('posts/edit_post.html', form=form)

@posts.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        try:
            db.session.add(post)
            db.session.commit()
            flash('Your post is now live!')
            return redirect(url_for('posts.index'))
        except:
            redirect('posts.create') 

    q = request.args.get('q')
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page) 
    else:
        page = 1 
    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q).all())
    else:
        posts = Post.query.order_by(Post.created.desc())
        
    pages = posts.paginate(page=page, per_page=app.config['POSTS_PER_PAGE'])
    # max pages = posts.count() or 404
    return render_template('posts/index.html', form=form, pages=pages)

@posts.route('/<slug>')
@login_required
def post_detail(slug):
    post = Post.query.filter(Post.slug==slug).first()
    tags = post.tags
    return render_template('posts/post_detail.html', post=post, tags=tags)

@posts.route('/tag/<slug>')
@login_required
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug==slug).first()
    posts = tag.posts.all()
    return render_template('posts/tag_detail.html', tag=tag, posts=posts)

