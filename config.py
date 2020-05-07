import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Configuration(object):
    # DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SECURITY_PASSWORD_SALT = 'salt'
    # SECURITY_PASSWORD_HASH = 'sha512_crypt'
    
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