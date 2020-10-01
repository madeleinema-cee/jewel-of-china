from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret_keys['secret_key']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = config.secret_keys['recap_public_key']
app.config['RECAPTCHA_PRIVATE_KEY'] = config.secret_keys['recap_private_key']

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = config.email['user']
app.config['MAIL_PASSWORD'] = config.email['password']
mail = Mail(app)


from flaskwebsite import routes
