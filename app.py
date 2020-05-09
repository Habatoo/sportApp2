from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail
from flask_moment import Moment

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from time import time

#from flask_security import SQLAlchemySessionUserDatastore
#from flask_security import Security

from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)

db  = SQLAlchemy(app)
mail = Mail(app)
moment = Moment(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

login = LoginManager(app)
login.login_view = 'login'

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='sportApp',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'): 
        os.mkdir('logs')
    file_handler = RotatingFileHandler(
        'logs/sportapp_{}.log'.format(str(int(time()))),
        maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('sportApp')

#### ADMIN ####
from models import *
admin = Admin(app)
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(Photo, db.session))

### Flask-security ###

# user_datastore = SQLAlchemySessionUserDatastore(db, User, Role)
# security = Security(app, user_datastore)
