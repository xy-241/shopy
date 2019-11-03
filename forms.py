from flask_wtf import FlaskForm # wheels made by others
from wtforms import StringField, PasswordField, SubmitField, BooleanField # for string field, for password field, for submit button, for remember password
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError  # Data is required, certain length, verifies email, for confirm password, for ensuring not duplicated values


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

class LoginForm(FlaskForm):
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")
