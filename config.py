import os
import urllib
import psycopg2

basedir = os.path.abspath(os.path.dirname(__file__))

class Configuration(object):
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
       'sqlite:///' + os.path.join(basedir, 'app.db')
    # try:
    #     SQLALCHEMY_DATABASE_URI = r'postgres://qkwtzbjxghqiyw:4ec57309b031383d02a5563c0e08bc86f17ee49af4dcac632ad53b02d4eac0d1@ec2-54-88-130-244.compute-1.amazonaws.com:5432/d2pcjnksf487v1'
    # except:
    #     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #         'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MAX_CONTENT_LENGTH = 16 * 1024 * 1024



class DevConfig(Configuration):
    ENV = 'development'
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
       'sqlite:///' + os.path.join(basedir, 'app.db')


    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # params = urllib.parse.quote_plus(
    #     r'DRIVER={SQL Server};SERVER=ec2-54-88-130-244.compute-1.amazonaws.com;DATABASE=d2pcjnksf487v1;UID=qkwtzbjxghqiyw;PWD=4ec57309b031383d02a5563c0e08bc86f17ee49af4dcac632ad53b02d4eac0d1;')
    # SQLALCHEMY_DATABASE_URI = r'postgres://qkwtzbjxghqiyw:4ec57309b031383d02a5563c0e08bc86f17ee49af4dcac632ad53b02d4eac0d1@ec2-54-88-130-244.compute-1.amazonaws.com:5432/d2pcjnksf487v1'
    SECRET_KEY = 'something very secret'

    DATA_DIR = os.environ.get('DATA_DIR') or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app\\static\\user_data\\') # 

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    
    MAIL_SERVER = 'localhost' or os.environ.get('MAIL_SERVER')
    MAIL_PORT = 8025 or int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']

    POSTS_PER_PAGE = 3

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