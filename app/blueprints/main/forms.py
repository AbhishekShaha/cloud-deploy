from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Required, Length, Email
from wtforms import ValidationError
from app.models import User


class BookForm(FlaskForm):
	name = StringField('Book Title', validators=[Required(), Length(1, 64)])
	author = StringField('Book Author', validators=[Required(), Length(1,128)])
	description = StringField('Description', validators=[Required(), Length(1,128)])
	submit = SubmitField('Create Book')


class ReviewForm(FlaskForm):
	body = StringField('Review', validators=[Required()])
	rating = IntegerField('Rating (1-5)', validators=[Required()])
	submit = SubmitField('Submit Review')

	
	def validate_rating(self, field):
		if field.data < 1 or field.data > 5:
			raise ValidationError('Rating Must Be Between 1-5')

class EnquiryForm(FlaskForm):
	email = StringField('Contact Email', validators=[Required(), Length(1,64), Email()])
	subject = StringField('Subject', validators=[Required(), Length(1,64)])
	body = StringField('Enquiry', validators=[Required()])
	submit = SubmitField('Submit Enquiry')