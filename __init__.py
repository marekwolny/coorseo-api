from __future__ import absolute_import, print_function

from flask import (Flask)
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from .views import home
from .views import courses
from .views import platforms
from .views import publishers
from .views import profile

from .models import db_session

app = Flask(__name__, static_url_path='/static')
app.config['TESTING'] = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['JSON_SORT_KEYS'] = False

app.register_blueprint(home.mod)
app.register_blueprint(courses.mod)
app.register_blueprint(platforms.mod)
app.register_blueprint(publishers.mod)
app.register_blueprint(profile.mod)


@app.teardown_request
def remove_db_session(exception):
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
