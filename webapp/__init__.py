from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'itIsMySecretKey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webapp.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    #Blueprint
    from .todos import todos
    from .auth import auth

    app.register_blueprint(todos, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #Database initialize
    from .models import User, Todo

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app