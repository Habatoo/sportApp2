import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Configuration(object):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.yandex.com' #os.environ.get('MAIL_SERVER')
    MAIL_PORT = 8025
    MAIL_USE_TLS = 1 #os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_ADMIN = os.environ.get('MAIL_ADMIN')

    POSTS_PER_PAGE = 2