from flask import Flask, render_template, url_for, flash, redirect
from flask_login import current_user, login_required
from . import main as main_blueprint
from app.blueprints.main.forms import BookForm, ReviewForm
from app.utils.decorators import admin_required
from app.models import Book, Permission, Review, User
from app import db
from sqlalchemy import func


@main_blueprint.route('/', methods=['GET'])
def index():
	books = Book.query.all()
	return render_template('main/index.html', books=books)

@main_blueprint.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('main/user.html', user=user)


@main_blueprint.route('/book/<int:id>', methods=['GET', 'POST'])
def book(id):
	book = Book.query.get_or_404(id)
	reviews = book.reviews
	form = ReviewForm()

	if form.validate_on_submit():
		if not current_user.is_authenticated:
			flash('You Must Have a Confirmed Account Before Submitting a Review.')

		elif current_user.is_authenticated and not current_user.confirmed:
			flash('You Must Confirm Your Account Before Submitting a Review.')

		else:
			review = Review(body=form.body.data, rating=form.rating.data, reviewer=current_user._get_current_object(), 
							book=book)
			total_rating = Review.query.with_entities(func.sum(Review.rating).label("rating")).filter_by(book=book).first()
			book.average = round((total_rating[0] / book.reviews.count()))
			db.session.add(review, book)
			return redirect(url_for('main.book', id=id))	
	return render_template('main/book.html', book=book, reviews=reviews, form=form)



@main_blueprint.route('/add-book', methods=['GET','POST'])
def add_book():
	form = BookForm()
	if current_user.is_authenticated and current_user.confirmed \
		and form.validate_on_submit():
		book = Book(name=form.name.data, author=form.author.data, description=form.description.data)
		db.session.add(book)
		return redirect(url_for('main.index'))
	return render_template('main/add_book.html', form=form)
