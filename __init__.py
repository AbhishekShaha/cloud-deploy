from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

	#instantiate application
	app = Flask(__name__)

	app_settings = os.getenv('APP_SETTINGS')
	app.config.from_object(app_settings)

	#set up extensions
	db.init_app(app)

	from app.blueprints.authgwy import authgwy
	app.register_blueprint(authgwy, url_prefix='/authgwy')

	from app.blueprints.main import main
	app.register_blueprint(main)

	return app