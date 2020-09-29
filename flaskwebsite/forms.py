from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import data_required, length, email, equal_to, ValidationError
from flaskwebsite.models import User, Tag


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
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username already exists. Please use another one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email already exists. Please use another one.')

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


class SearchForm(FlaskForm):
    search_text = StringField('Search...', validators=[data_required(), length(min=1, max=30)])
    submit1 = SubmitField('Search')


class TagField(StringField):
    '''
    Tag field taken from "Learning Flask Framework" by Matt CopperWaite and Charles Leifer
    Check out pages 37-42
    Copperwaite, Matt, and Charles Leifer. 2015. Learning Flask Framework.
    Packt Publishing. http://www.totalboox.com/book/id-7553921423834771450.
    '''

    def _value(self):
        if self.data:
            return ', '.join([tag.name for tag in self.data])
        return ''

    def get_tags_from_string(self, tag_string):
        raw_tags = tag_string.split(',')

        tag_names = [name.strip() for name in raw_tags if name.strip()]

        existing_tags = Tag.query.filter(Tag.name.in_(tag_names))

        new_names = set(tag_names) - set([tag.name for tag in existing_tags])

        new_tags = [Tag(name=name) for name in new_names]

        return list(existing_tags) + new_tags

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.get_tags_from_string(valuelist[0])
        else:
            self.data = []


class PostForm(FlaskForm):
    title = StringField('Title', validators=[data_required()])
    chinese_content = TextAreaField('Chinese Text')
    content = TextAreaField('Content', validators=[length(min=2)])
    tags = TagField("Tags", validators=[length(min=1, max=30)])
    recap = RecaptchaField()
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    name = StringField('Name', validators=[length(max=20)])
    comments = TextAreaField('Comments', validators=[length(min=2)])
    recap = RecaptchaField()
    submit2 = SubmitField('Send')

