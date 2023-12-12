from flask_login import UserMixin
from . import db
from datetime import datetime
from flask_bcrypt import Bcrypt
import os
import uuid
from sqlalchemy.orm import relationship
from .utils import generate_unique_filename
from flask import current_app

bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(255), default='userposts/default_profile.jpg')
    bio = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)
    followers = db.relationship('Follow', foreign_keys='Follow.followed_id', backref='followed_user', lazy='dynamic')
    following = db.relationship('Follow', foreign_keys='Follow.follower_id', backref='follower_user', lazy='dynamic')

    def post_count(self):
        return len(self.posts)

    def followers_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def like(self, post_id):
        if not self.has_liked(post_id):
            new_like = Like(author_id=self.id, post_id=post_id)
            db.session.add(new_like)
            db.session.commit()

    def unlike(self, post):
        like = Like.query.filter_by(author_id=self.id, post_id=post.id).first()
        if like:
            db.session.delete(like)
            db.session.commit()

    def has_liked(self, post_id):
        return Like.query.filter_by(author_id=self.id, post_id=post_id).count() > 0

    def is_following(self, user):
        return Follow.query.filter_by(follower_id=self.id, followed_id=user.id).count() > 0

    def follow(self, user_to_follow):
        if not self.is_following(user_to_follow) and self != user_to_follow:
            new_follow = Follow(follower_id=self.id, followed_id=user_to_follow.id)
            db.session.add(new_follow)

    def unfollow(self, user_to_unfollow):
        follow_relationship = Follow.query.filter_by(follower_id=self.id, followed_id=user_to_unfollow.id).first()
        if follow_relationship:
            db.session.delete(follow_relationship)

    def get_followed_posts(self, page=1, per_page=70):
        followed = Follow.query.filter_by(follower_id=self.id).all()
        followed_ids = [followed_user.followed_id for followed_user in followed]
        followed_ids.append(self.id)
        return Post.query.filter(Post.author_id.in_(followed_ids)).order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page)

    def save_profile_picture(self, image_file, upload_folder):
        _, file_extension = os.path.splitext(image_file.filename)
        file_extension = file_extension.lower().lstrip('.')
        allowed_extensions = {'jpg', 'jpeg', 'gif', 'png'}

        if file_extension not in allowed_extensions:
            raise ValueError('Invalid image file extension')

        print(f"Received file with extension: {file_extension}")
        print(f"Upload folder: {upload_folder}")

        try:
            unique_filename = generate_unique_filename(self.username, file_extension)
            image_path = os.path.join(upload_folder, unique_filename)
            image_file.save(image_path)
            self.profile_picture = f'userposts/{unique_filename}'
            print("File saved successfully.")
        except Exception as e:
            print(f"Error saving file: {e}")
            raise ValueError('Error saving image file')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_type = db.Column(db.String(20), nullable=False)
    post_content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)

    def generate_unique_filename(self, file_extension):
        return generate_unique_filename(self.author.username, file_extension)

    def save_image(self, image_file, upload_folder):
        _, file_extension = os.path.splitext(image_file.filename)
        print(f"File extension: {file_extension}")

        file_extension = file_extension.lower().lstrip('.')
        allowed_extensions = {'jpg', 'jpeg', 'gif', 'png'}

        if file_extension not in allowed_extensions:
            raise ValueError('Invalid image file extension')

        unique_filename = self.generate_unique_filename(file_extension)
        image_path = os.path.join(upload_folder, unique_filename)
        image_file.save(image_path)
        self.post_content = f'userposts/{unique_filename}'

    def save_video(self, video_file, upload_folder):
        unique_filename = self.generate_unique_filename('mp4')
        video_path = os.path.join(upload_folder, unique_filename)
        video_file.save(video_path)
        self.post_content = f'userposts/{unique_filename}'
        db.session.add(self)

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, follower_id=None, followed_id=None):
        self.follower_id = follower_id
        self.followed_id = followed_id

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    comment_content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime)