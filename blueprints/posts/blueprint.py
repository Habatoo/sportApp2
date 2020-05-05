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

# @posts.route('/create', methods=['GET', 'POST'])
# @login_required
# def create_post():
#     form = PostForm()
#     if request.method == 'POST':
#         post = Post(body=form.post.data, author=current_user, title=form.title.data)
#         try:
#             db.session.add(post)
#             db.session.commit()
#             flash('Your post is now live!')
#             return redirect(url_for('posts.index'))
#         except:
#            redirect('posts.create') 
#     return render_template('posts/create_post.html', form=form)

@posts.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('posts.index'))
    q = request.args.get('q')
    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q).all())
    else:
        posts = Post.query.order_by(Post.created.desc())
        
    return render_template('posts/index.html', posts=posts, form=form)

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

