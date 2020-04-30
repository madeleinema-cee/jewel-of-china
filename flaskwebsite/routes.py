from flask import render_template, redirect, url_for, flash
from flaskwebsite import app, db
from flaskwebsite.models import User
from flaskwebsite.forms import RegistrationForm, LoginForm


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html', title= 'About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login',  methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('You have logged in!')
        return redirect(url_for('home'))
    else:
        flash('Login Unsuccessful. Please check again!', 'danger')
    return render_template('login.html', title='login', form=form)

