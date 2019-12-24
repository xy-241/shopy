from flask_wtf import FlaskForm # wheels made by others
from wtforms import StringField, PasswordField, SubmitField, BooleanField # for string field, for password field, for submit button, for remember password
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError  # Data is required, certain length, verifies email, for confirm password, for ensuring not duplicated values

from shopyP.models import User

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
    def validateUsername(self, username):
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
