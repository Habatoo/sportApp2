from app import app
from app import db

from blueprints.posts.blueprint import posts
from blueprints.users.blueprint import users
from blueprints.events.blueprint import events
from blueprints.photos.blueprint import photos

import view
import errors

app.register_blueprint(posts, url_prefix='/post')
app.register_blueprint(users, url_prefix='/user')
app.register_blueprint(events, url_prefix='/event')
app.register_blueprint(photos, url_prefix='/photo')

if __name__ == '__main__':
    app.run()