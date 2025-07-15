import os
from flask import Flask
from flask_login import LoginManager

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)
   
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .db import get_db

    @login_manager.user_loader
    def load_user(user_id):
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        if user:
            class User:
                def __init__(self, id, username):
                    self.id = id
                    self.username = username
                def is_active(self):
                    return True
                def get_id(self):
                    return str(self.id)
                def is_authenticated(self):
                    return True
            return User(user['id'], user['username'])
        return None

    return app