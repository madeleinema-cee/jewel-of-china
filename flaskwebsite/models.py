from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer
from flaskwebsite import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


tags = db.Table('tags',
                db.Column('post_id', db.Integer, db.ForeignKey('post.post_id')),
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.tag_id'))
                )


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    chinese_content = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_comments = db.Column(db.Integer, nullable=True)
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('post_tags', lazy='dynamic'))
    comments = db.relationship('Comment', backref='comments', lazy=True)


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', ‘{self.tags}’)"


class Tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),  nullable=False)
    date_commented = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comment = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
