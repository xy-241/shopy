from flask_wtf import FlaskForm # wheels made by others
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, SelectField, TextAreaField, IntegerField # for string field, for password field, for submit button, for remember password
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError  # Data is required, certain length, verifies email, for confirm password, for ensuring not duplicated values

from flask_wtf.file import FileField, FileAllowed # The type of th field, and what type of file is allowed
from flask_login import current_user # Indicate current user

from shopyP.models import User, Admin, HackingProduct


class RegistrationForm(FlaskForm):
    username = StringField('Username',  #Username is shown in html, the label method
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password')]) #Equal to previous password
    submit = SubmitField('Sign Up')

    # Ensure no duplicated usename
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose a different one!")
    # Ensure no duplicated email
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one!")
class LoginForm(FlaskForm):
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

# ZiMing
class addForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    price = DecimalField('Price', places=2, rounding=None, use_locale=False, number_format=None, validators=[DataRequired()])
    itemNum = IntegerField('Stock', validators=[DataRequired()])
    picture = FileField('Product Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    category = SelectField('Category', validators=[DataRequired()], choices=[('outfits', 'Outfit'),('tools', 'Tool')], default='Outfit')
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_title(self, title):
        title = HackingProduct.query.filter_by(title=title.data).first()
        if title:
            raise ValidationError("That title is taken. Please choose a different one!")

class updateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    price = DecimalField('Price', places=2, rounding=None, use_locale=False, number_format=None, validators=[DataRequired()])
    itemNum = IntegerField('Stock', validators=[DataRequired()])
    picture = FileField('Product Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    category = SelectField('Category', validators=[DataRequired()], choices=[('outfits', 'Outfit'),('tools', 'Tool')], default='Outfit')
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Update')
# ZiMing

# JT
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
# JT

#Checkout Form (Kenneth)
class CheckoutForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired()], render_kw={"placeholder": "John"})
    lastName = StringField('Last Name', validators=[DataRequired()], render_kw={"placeholder": "Doe"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "johndoe@gmail.com"})
    address = StringField('Address', validators=[DataRequired()], render_kw={"placeholder": "180 Ang Mo Kio Ave 8"})
    postal = StringField('Postal Code', validators=[DataRequired()], render_kw={"placeholder": "569830"})
    cardName = StringField('Name on Card', validators=[DataRequired()], render_kw={"placeholder": "John Doe"})
    cardNumber = StringField('Card Number', validators=[DataRequired()], render_kw={"placeholder": "1111-2222-3333-4444"})
    expDate = StringField('Exp Month', validators=[DataRequired()], render_kw={"placeholder": "Apr/25"})
    cvv = IntegerField('CVV', validators=[DataRequired()], render_kw={"placeholder": "123"})
#Checkout Form (Kenneth)
