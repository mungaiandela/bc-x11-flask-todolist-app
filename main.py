import os

from flask import Flask, flash, redirect, url_for, render_template
from flask_login import login_user, logout_user, current_user
from flask_migrate import Migrate
from flask_restful import Api

from app import models
from app.models import db
from app.models import lm
from app.models import User
from config import app_configuration
# from app.views.assets import AssetResource

from oauth import OAuthSignIn

def create_app(environment):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_configuration[environment])
    app.secret_key = os.getenv("SECRET_KEY")

    db.init_app(app)
    lm.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    # api.add_resource(AssetResource,
    #                  '/api/v1/assets', '/api/v1/assets/',
    #                  endpoint='assets')

    @lm.user_loader
    def load_user(id):  
        return User.query.get(int(id))

    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))


    @app.route('/authorize/<provider>')
    def oauth_authorize(provider):
        if not current_user.is_anonymous:
            return redirect(url_for('index'))
        oauth = OAuthSignIn.get_provider(provider)
        return oauth.authorize()


    @app.route('/callback/<provider>')
    def oauth_callback(provider):
        if not current_user.is_anonymous:
            return redirect(url_for('index'))
        oauth = OAuthSignIn.get_provider(provider)
        social_id, username, email = oauth.callback()
        if social_id is None:
            flash('Authentication failed.')
            return redirect(url_for('index'))
        user = models.User.query.filter_by(social_id=social_id).first()
        if not user:
            user = models.User(social_id=social_id, nickname=username, email=email)
            db.session.add(user)
            db.session.commit()
        login_user(user, True)
        return redirect(url_for('index'))

    return app
app = create_app(os.getenv("FLASK_CONFIG"))

if __name__ == "__main__":
    app = create_app(os.getenv("FLASK_CONFIG"))
    app.run()
