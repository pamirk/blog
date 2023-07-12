from datetime import datetime
from hashlib import md5

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # followers and followed are defined as the left and right sides of the relationship.
    # The relationship between the left and right sides is defined by the association table.
    # The secondary argument indicates the association table that is used for this relationship.
    # The primaryjoin argument indicates the condition that links the left side entity
    # (the follower user) with the association table. The followers.c.follower_id
    # expression references the follower_id column of the association table.
    # Similarly, the secondaryjoin argument indicates the condition that links the right
    # side entity (the followed user) with the association table. The followers.c.followed_id
    # expression references the followed_id column of the association table.
    # The backref argument defines how this relationship will be accessed from the right
    # side entity. From the left side, the relationship is named followed, so from the right
    # side I have to use the name followers to represent all the left side users that are
    # linked to the target user on the right side.
    # The lazy argument indicates the execution mode for this query. A mode of dynamic
    # sets up the query to not run until specifically requested, which is useful for
    # applying additional filters to the query before accessing the results.
    # The cascade argument configures the delete-orphan cascade mode, which deletes
    # a follower when it is removed from the association table.
    # The order_by argument instructs the database to sort the left side entity by the
    # date of the association table in descending order, so the most recent followers
    # are returned first.
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),  # left side entity
        secondaryjoin=(followers.c.followed_id == id),  # right side entity
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')  # right side entity

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


@login.user_loader
def load_user(userid):
    return User.query.get(int(userid))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
