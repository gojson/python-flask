#encoding: utf-8


#供模型使用 db.Model
from exts import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tel = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(32),nullable=False)
    pwd = db.Column(db.String(100),nullable=False)
    created_at = db.Column(db.DateTime,nullable=False)


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)

    #now()获取服务器第一次运行的时间
    #now 每次创建一个模型时候,都获取当前的时间
    created_at = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('User.id'))
    #反转
    author = db.relationship('User',backref=db.backref('questions'))
