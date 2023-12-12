from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .utils import generate_unique_filename
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config['SECRET_KEY'] = 'aabbccddeeffgg'
    app.config['UPLOAD_FOLDER'] = '/var/lib/docker/volumes/interactify_userposts/static/userposts'

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/lib/docker/volumes/interactify_data/interactify.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    db.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('auth.unauthorized'))

    from .views import views
    from .auth import auth
    from website import models

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        db.create_all()

    return app