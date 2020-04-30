from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import data_required, length, email, equal_to



class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[data_required(), length(min=2, max=20)])
    email = StringField('Email',
                        validators=[email(), data_required()])
    password = PasswordField('Password',
                             validators=[data_required()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[data_required(), equal_to('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[email(), data_required()])
    password = PasswordField('Password',
                             validators=[data_required()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')