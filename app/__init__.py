import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
moment = Moment()
bootstrap = Bootstrap()
mail = Mail()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(ctx='app.config.DevelopmentConfig'):

	#instantiate application
	app = Flask(__name__)


	#app_settings = os.getenv(ctx)
	app.config.from_object(ctx)

	#set up extensions
	db.init_app(app)
	moment.init_app(app)
	bootstrap.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from app.blueprints.auth import auth
	app.register_blueprint(auth, url_prefix='/auth')

	from app.blueprints.main import main
	app.register_blueprint(main)

	return app