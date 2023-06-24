from sqlalchemy import BigInteger, Boolean, Column, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from flaskblog import db, login_manager
from flask_login import UserMixin
from datetime import datetime
import flask_whooshalchemy as wa

@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __searchable__ = ['name', 'screenname']

    userid = Column(db.BigInteger, primary_key=True)
    name = Column(db.Text, nullable=False)
    screenname = Column(db.Text, nullable=False)
    location = Column(db.Text, nullable=False)
    description = Column(db.Text, nullable=False)
    verified = Column(db.Boolean, nullable=False)
    income = Column(db.BigInteger, nullable=False)
    age = Column(db.BigInteger, nullable=False)
    hobby = Column(db.Text, nullable=False)

    def get_id(self):
        return (self.userid)


class Following(db.Model):
    __tablename__ = 'following'

    userid = Column(db.BigInteger, primary_key=True, nullable=False)
    followerid = Column(db.BigInteger, primary_key=True, nullable=False)

    def get_id(self):
        return (self.userid)


class Isrelated(db.Model):
    __tablename__ = 'isrelated'

    userid = Column(db.BigInteger, primary_key=True, nullable=False)
    relateduserid = Column(db.BigInteger, primary_key=True, nullable=False)
    type = Column(db.Text, nullable=False)

    def get_id(self):
        return (self.userid)


class Post(db.Model):
    __tablename__ = 'post'

    postid = Column(db.BigInteger, primary_key=True)
    userid = Column(db.BigInteger, nullable=False)
    createdat = Column(db.DateTime, nullable=False)
    message = Column(db.Text, nullable=False)

    def get_id(self):
        return (self.postid)
