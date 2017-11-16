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
	POSTGRES_DB_USER = os.getenv('POSTGRES_DB_USER')
	POSTGRES_DB_PASSWORD = os.getenv('POSTGRES_DB_PASSWORD')
	POSTGRES_DB_HOST = os.getenv('POSTGRES_DB_HOST')


class DevelopmentConfig(BaseConfig):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres'


class TestingConfiguration(BaseConfig):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')
	TESTING = True