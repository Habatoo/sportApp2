from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from .forms import EditProfileForm

from app import app, log
from app import db
from app.models import *

users = Blueprint('users', __name__, template_folder='templates')


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.created.desc())
    pages = posts.paginate(page=page, per_page=app.config['POSTS_PER_PAGE'])

    events = user.events.order_by(Event.created.desc())
    event_pages = events.paginate(page=page, per_page=app.config['POSTS_PER_PAGE'])

    return render_template('users/index.html', user=user, pages=pages, event_pages=event_pages)

@users.route('/tag/<slug>')
@login_required
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug==slug).first()
    users = tag.users_tags.all()
    return render_template('users/tag_detail.html', tag=tag, users=users)


@users.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.city = form.city.data
        current_user.tags.append(Tag.query.filter_by(name=form.tags.data).first())
        db.session.commit()
        flash('Your changes have been saved.')
        log.info("User '%s' edit profile." % (current_user.username))
        return redirect(url_for('user', username=current_user.username))
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
        return redirect(url_for('users.index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('users.index', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    log.info("User '%s' following user '%s'." % (current_user.username, username))
    return redirect(url_for('posts.index', username=username))


@users.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('users.index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('users.index', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    log.info("User '%s' unfollowing user '%s'." % (current_user.username, username))
    return redirect(url_for('posts.index', username=username))