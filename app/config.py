import os


class BaseConfig():
	WTF_CSRF_ENABLED = True
	SSL_DISABLE = True
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_RECORD_QUERIES = True
	SECRET_KEY = os.getenv('SECRET_KEY')
	SITE_ADMIN = os.getenv('SITE_ADMIN')
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('SITE_ADMIN')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


class DevelopmentConfig(BaseConfig):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL')


class TestingConfiguration(BaseConfig):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')
	TESTING = True