import hashlib, bleach
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request, url_for, flash
from flask_login import UserMixin, AnonymousUserMixin
from app import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown

# hex values to represent permission. 1 byte = 8 bits only 5 currently used.
class Permission:
	WRITE_REVIEWS= 0x01
	COMMENT = 0x02
	UPLOAD_BOOKS= 0x04
	MODERATE_COMMENTS = 0x08
	ADMINISTRATOR = 0x80

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	default = db.Column(db.Boolean, default=False, index=True)
	permissions = db.Column(db.Integer)
	users = db.relationship('User', backref='role', lazy='dynamic')

	@staticmethod
	def insert_roles():
		roles = {
			'User': (Permission.WRITE_REVIEWS,True),
			'Administrator': (0xff, False)
		}

		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			db.session.add(role)
		db.session.commit()


class User(UserMixin, db.Model):
	# Defines the User model that will be used.
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	password_hash = db.Column(db.String(128))
	confirmed = db.Column(db.Boolean, default=False)
	location = db.Column(db.String(64))
	name = db.Column(db.String(64))
	avatar_hash = db.Column(db.String(32))
	member_since = db.Column(db.DateTime(), default=datetime.utcnow)
	last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
	reviews = db.relationship('Review', backref='reviewer', lazy='dynamic')


	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		if self.role is None:
			if self.email == current_app.config['SITE_ADMIN']:
				self.role = Role.query.filter_by(permissions=0xff).first()
			if self.role is None:
				self.role = Role.query.filter_by(default=True).first()
			if self.email is not None and self.avatar_hash is None:
				self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()


	def gravatar(self, size=100, default='identicon', rating='g'):
		if request.is_secure:
			url = 'https://secure.gravatar.com/avatar'
		else:
			url = 'http://www.gravatar.com/avatar'
		hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
		return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		"""
		Encrypts user password so to not store passwords in plain text.
		:param self: User object in context.
		:param password: password that is passed in from Form.
		"""
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		"""
		Verifies password is correct using the password hash.
		:param self: User object in context.
		:param password: password that is passed in from Form.

		:return: Boolean
		"""
		return check_password_hash(self.password_hash, password)

	def generate_confirmation_token(self, expiration=3600):

		print(self.email)
		print(self.id)
		"""
		Generates a confirmation token what will be sent as part of an email for registering a User.
		:param: self: User object.
		:param: expiration: How long before the token will expire. Defaults to 3600 seconds.

		:return: a serialized token.
		"""
		s = Serializer(current_app.config['SECRET_KEY'], expiration)

		token = s.dumps({'confirm': self.id})

		data = s.loads(token)

		print(data)

		return s.dumps({'confirm': self.id})

	def confirm(self, token):
		"""
		Used to confirm the token is valid.
		:param: self: User object.
		:param: token: Token being passed in to confirm is valid.

		:return: Boolean
		"""
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('confirm') != self.id:
			return False

		self.confirmed = True
		db.session.add(self)
		return True

	def generate_reset_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'reset': self.id})

	def reset_password(self, token, new_password):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('reset') != self.id:
			return False
		self.password = new_password
		db.session.add(self)
		return True

	def can(self, permissions):
		return self.role is not None and (self.role.permissions & permissions) == permissions

	def is_administrator(self):
		return self.can(Permission.ADMINISTRATOR)

	def ping(self):
		self.last_seen = datetime.utcnow()
		db.session.add(self)


class AnonymousUser(AnonymousUserMixin):
	def can(self, permissions):
		return False

	def is_administrator(self):
		return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
	# loads User object by id (Required callback by flask_login)
    return User.query.get(int(user_id))

class Book(db.Model):
	__tablename__ = 'books'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128))
	average = db.Column(db.Integer)
	author = db.Column(db.String(128))
	description = db.Column(db.String(128))
	reviews = db.relationship('Review', backref='book', lazy='dynamic')

class Review(db.Model):
	__tablename__ = 'reviews'
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	rating = db.Column(db.Integer)
	reviewer_id = db.Column(db.Integer, db.ForeignKey(User.id))
	book_id = db.Column(db.Integer, db.ForeignKey(Book.id))