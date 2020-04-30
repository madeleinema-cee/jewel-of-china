from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'bd95b20cb68c470de174216f1ead5b9c'
app.config['SQLALCHEMY_DATAEBASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)



from flaskwebsite import routes