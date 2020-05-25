from datetime import datetime
from werkzeug.urls import url_parse
import os
import logging

from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from flask_login import login_user, logout_user, current_user, login_required

from app import app, db, log
from app.models import *
from app.copydir import copydir
from app.email import send_password_reset_email

# log = logging.getLogger('btb_Api')
# fh = logging.FileHandler(app.config['LOGGER_CONFIG']['file'])
# fh.setLevel(app.config['LOGGER_CONFIG']['level'])
# fh.setFormatter(app.config['LOGGER_CONFIG']['formatter'])
# log.addHandler(fh)
# log.setLevel(app.config['LOGGER_CONFIG']['level'])

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/admin/')
@login_required
def admin():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    if user.username != 'admin':
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
    page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Incorrect email or password.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        log.info("User '%s' login." % (user.username))
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    user = current_user.username
    logout_user()
    log.info("User '%s' logout." % (user))
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data, 
            email=form.email.data, 
            city=form.city.data
            )
        user.set_password(form.password.data)
        log.debug("user before: %s", user)
        try:
            db.session.add(user)
            db.session.commit()
            log.debug("user after: %s", user)
            new_user = User.query.filter(User.username == form.username.data).first()         
            user_dir = new_user.username + new_user.timestamp
            user_folders = os.path.join('app', 'static', 'user_data', user_dir)
            if not os.path.isdir(user_folders):
                os.mkdir(user_folders)
                os.mkdir(os.path.join(user_folders, 'photos'))
                os.mkdir(os.path.join(user_folders, 'tracking_data'))
            copydir(os.path.join('app', 'static', 'user_data', 'avatar'), user_folders)
            flash('Congratulations, you are now a registered user!')
            log.debug("user after make folder: %s", user)
            log.info("User '%s' register." % (user.username))
            return redirect(url_for('login'))
        except:
            flash('Something wrong')
            log.info("User '%s' can not register." % (user.username))
            return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        log.info("User with  email '%s' reset password." % (form.email.data))
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

