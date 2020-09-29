from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bd95b20cb68c470de174216f1ead5b9c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Len_c0ZAAAAAIqon7rDn4vCUb_fEqudOInJ_hwO'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Len_c0ZAAAAAKCYf6BRGYrUEcU3nF3ExZjxVQdl'

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'email'
app.config['MAIL_PASSWORD'] = 'password'
mail = Mail(app)


from flaskwebsite import routes
