# create database models
from exts import db
from datetime import datetime


# the database for storing the verification code of each email address
# email, verification code
# id as primary key
class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    verification_code = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.Date, default=datetime.now)


# the database for storing the information of each user
# username, email, password
# id as primary key
class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    verification_code = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(400), nullable=False)
    available_time = db.Column(db.Date, default=datetime.now)


# the database for storing the information of each todolist
# assessment title, module, deadline, importance, status, description
# id as primary key, author id as foreign key
class PostModel(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    pic = db.Column(db.String(20000), nullable=False)
    category = db.Column(db.String(200), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)
    popular = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.Date, default=datetime.now)
    # use foreign keys to reference other form content
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship(UserModel, backref="posts")


class CollectionModel(db.Model):
    __tablename__ = "collection"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    post = db.relationship(PostModel, backref="collections")
    author = db.relationship(UserModel, backref="collections")


class CommentModel(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.Date, default=datetime.now)
    # foreign keys
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # relationship
    post = db.relationship(PostModel, backref=db.backref("comments", order_by=create_time.desc()))
    author = db.relationship(UserModel, backref="comments")

