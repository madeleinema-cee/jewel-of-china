from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import data_required, length, email, equal_to, ValidationError
from flaskwebsite.models import User


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

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username already exists. Please use another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email already exists. Please use another one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[email(), data_required()])
    password = PasswordField('Password',
                             validators=[data_required()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[data_required(), length(min=2, max=20)])
    email = StringField('Email',
                        validators=[email(), data_required()])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username already exists. Please use another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email already exists. Please use another one.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[data_required()])
    content = TextAreaField('Content', validators=[data_required()])
    submit = SubmitField('Post')


class RequestResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[data_required(), email()])
    submit = SubmitField('Request Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('That email is not registered, please register an account first!')


class ResetPasswordForm(FlaskForm):
    password = StringField('New Password', validators=[data_required()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[data_required(), equal_to('password')])
    submit = SubmitField('Reset Password')
