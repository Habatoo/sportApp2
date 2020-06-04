import os
import urllib
import psycopg2
import logging

basedir = os.path.abspath(os.path.dirname(__file__))


class Configuration(object):
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
       'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 3

    LOGGER_CONFIG = dict(level=logging.DEBUG,
                     file="app.log",
                     formatter=logging.Formatter("%(asctime)s [%(levelname)s] - %(name)s:%(message)s")
                     )

    ########## File upload config #############################
    # MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

    OAUTH_CREDENTIALS = os.environ.get('OAUTH_CREDENTIALS')


class DevConfig(Configuration):
    ENV = 'development'
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
       'sqlite:///' + os.path.join(basedir, 'app.db')


    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'something very secret'

    DATA_DIR = os.environ.get('DATA_DIR') or \
         os.path.join(
             os.path.dirname(os.path.abspath(__file__)), 'app', 'static', 'user_data') # 

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    
    MAIL_SERVER = 'localhost' or os.environ.get('MAIL_SERVER')
    MAIL_PORT = 8025 or int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']

    CITIES = [
        {'label': 'Novosibirsk', 'value': 'Novosibirsk'},
        {'label': 'Moscow', 'value': 'Moscow'},
        ]


class ProdConfig(Configuration):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')


config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
}