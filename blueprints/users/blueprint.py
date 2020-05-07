from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from .forms import EditProfileForm

from app import app
from models import *

users = Blueprint('users', __name__, template_folder='templates')

@users.route('/')
@login_required
def index():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    return render_template('users/index.html', user=user)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.created.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('users/index.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@users.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # form = EditProfileForm(current_user.username, formdata=request.form, obj=current_user)
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        # form.populate_obj(current_user)
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.city = form.city.data
        # current_user.tags = [form.tags.data]
        try:
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('users.index'))
        except:
            flash('Something wrong')
            return redirect(url_for('users.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('users/edit_profile.html', title='Edit Profile', form=form)


@users.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('users.user', username=username))


@users.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))