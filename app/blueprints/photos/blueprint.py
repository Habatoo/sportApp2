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

from .forms import PhotoForm

from app import app
from app import db
from app.models import *

import os

photos = Blueprint('photos', __name__, template_folder='templates')


@photos.route('/', methods=['GET', 'POST'])
@login_required
def index():
    args = {'method': 'GET'}
    # MAX_FILE_SIZE = 1024 * 1024 + 1

    user = User.query.filter(User.username == current_user.username).first()     
    user_dir = user.username + user.timestamp
    user_folders = os.path.join(app.config['DATA_DIR'], user_dir, 'photos')
    files_path = os.listdir(user_folders)
    img_url = ['user_data/{}/{}/{}'.format(user_dir, 'photos', files) for files in files_path]
  


    if request.method == 'POST':
        for file in request.files.getlist('file'):
            filename = file.filename
            # if bool(file.filename):
            #     file_bytes = file.read(MAX_FILE_SIZE)
            #     args['file_size_error'] = len(file_bytes) == MAX_FILE_SIZE
            # args['method'] = 'POST'
            destination = '/'.join([user_folders, filename])
            file.save(destination)

            photo = Photo(
            photo_title='', 
            photo_description='', 
            slug='user_data/{}/{}/{}'.format(user_dir, 'photos', filename),
            photo_author=current_user, 
            )
            db.session.add(photo)
            db.session.commit()

        return redirect(url_for('photos.index'))
    return render_template('photos/index.html', args=args, files_path=files_path, img_url=img_url)
    

@photos.route('/<slug>')
@login_required
def photo_detail(slug):
    photo = Photo.query.filter(Post.slug==slug).first()
    tags = post.tags
    return render_template('posts/post_detail.html', post=post, tags=tags, user=current_user)
