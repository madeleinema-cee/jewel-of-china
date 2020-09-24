import secrets
import os
from PIL import Image
from hanziconv import HanziConv
from flask import render_template, redirect, url_for, flash, request, abort
from flaskwebsite import app, db, bcrypt, mail
from flaskwebsite.models import User, Post, Tag
from flaskwebsite.forms import RegistrationForm, LoginForm,\
                                UpdateAccountForm, PostForm,\
                                RequestResetPasswordForm, ResetPasswordForm,\
                                SearchForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    count = Post.query.count()
    tags = Tag.query.all()

    search_form = SearchForm()
    if request.method == 'POST':
        if search_form.submit1.data and search_form.validate_on_submit():
            return redirect(url_for('search', query=search_form.search_text.data))

    return render_template('home.html', posts=posts, tags=tags, search_form=search_form)


@app.route('/search/<string:query>', methods=['GET', 'POST'])
def search(query):

    search_form = SearchForm()
    query = query.lower()
    posts = Post.query.filter(Post.title.contains(query) | (Post.content.contains(query))| (Post.chinese_content.contains(query))).all()

    tags = Tag.query.filter_by(name=query).all()
    if tags:
        return render_template('search.html', search_form=search_form, posts=posts, query=query, tags=tags)


    if request.method == 'POST':
        if search_form.validate_on_submit():
            return redirect(url_for('search', query=search_form.search_text.data))

    return render_template('search.html', search_form=search_form, posts=posts, query=query)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login Successful.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check again!', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account is updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        chinese = HanziConv.toTraditional(form.chinese_content.data)
        title = HanziConv.toTraditional(form.title.data)
        post = Post(author=current_user, title=title,
                    chinese_content=chinese, content=form.content.data,
                    tags=form.tags.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = HanziConv.toTraditional(form.title.data)
        post.chinese_content = HanziConv.toTraditional(form.chinese_content.data)
        post.content = form.content.data
        post.tags = form.tags.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.chinese_content.data = post.chinese_content
        form.content.data = post.content
        form.tags.data = post.tags
    return render_template('create_post.html', title='Update Post', form=form, legend="Update Post")


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route('/user/<string:username>')
def user_posts(username):
    tags = Tag.query.all()
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, tags=tags, user=user)


@app.route('/tag/<tag>')
def search_tag(tag):
    page = request.args.get('page', 1, type=int)
    tag = Tag.query.filter_by(name=tag).first_or_404()
    name = tag.name
    posts = tag.post_tags.order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('tag.html', tag_name=name, posts=posts)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='donotreply@info.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

if you did not make this request, please ignore this email.
    '''
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def request_reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('You requested reset the password! An email has been sent to you.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('request_reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been reset! You are now able to log in!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
